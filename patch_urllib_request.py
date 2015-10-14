import urllib.request

class RedirectWithCookieHandler(urllib.request.HTTPRedirectHandler):

    def http_error_302(self, req, fp, code, msg, headers):
        # print("Cookie Manip Right Here")
        return urllib.request.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)

    http_error_301 = http_error_303 = http_error_307 = http_error_302

cookieprocessor = urllib.request.HTTPCookieProcessor()

opener = urllib.request.build_opener(RedirectWithCookieHandler, cookieprocessor)
urllib.request.install_opener(opener)

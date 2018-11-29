#!/usr/bin/python2.6
# -*- coding: UTF-8 -*-
#
# -------------------------------------------
#
# @Name: detector
#
# @Describe:
#
#
# @Date:    2018-11-23
#
# @Author:  grapeisme
#
# -------------------------------------------
# CODE BEGINS
#
#

import sys
import urllib2
import json
import time
import argparse

import socket
urllib2.socket.setdefaulttimeout(10)

DEF_HTTP_SLEEP_S = 0.01

def wlog(s):
    tm = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    s = s.strip()
    print "[%s] %s" % (tm, s)


class Detector:
    def __init__(self, url, cand_headers, must_contain, post_data = ""):
        self.url = url
        self.cand_headers = cand_headers
        self.must_contain = must_contain
        self.post_data = post_data
        pass

    def http_get(self, headers, proxy_addr = ""):
        out = ""

        if self.post_data:
            request = urllib2.Request(self.url, postdata = post_data, headers = headers)
        else:
            request = urllib2.Request(self.url, headers = headers)

        if proxy_addr:
            proxy = urllib2.request.ProxyHandler({'http':proxy_addr})
            opener = urllib2.request.build_opener(proxy, urllib.request.HTTPHandler)
            urllib2.request.install_opener(opener)

        try:
            response = urllib2.urlopen(request)
            out = response.read()
        #except urllib2.HTTPError, e: 
        #    out = "HTTPError, code:%s" % e.code
        #    return False, out
        #except urllib2.URLError, e:
        #    out = "URLError, code:%s, error:%s" % (e.code, e.read())
        #    return False, out
        except Exception as e:
            out = "Exception, error:%s" % (e.args)
            return False, out

        return True, out 

    def is_content_ok(self, content):
        return content.find(self.must_contain) > -1

    def run(self):
        headers_flag = {}
        for k in self.cand_headers.keys():
            headers_flag[k] = 1

        has_ok = False
        for k in headers_flag.keys():
            headers = {}
            for (sk, sv) in self.cand_headers.items():
                if sk == k:     # try without k
                    continue
                if headers_flag.get(sk, 0) == 1:
                    headers[sk] = sv;

            time.sleep(DEF_HTTP_SLEEP_S)
            res, out = self.http_get(headers)

            if not res:
                wlog("HTTP_GET failed, try_without:%s, error:%s" % (k, out) )
                continue
            if not self.is_content_ok(out):
                wlog("CONTENT_NOT_OK, try_without:%s" % (k) )
                #wlog("CONTENT_NOT_OK, try_without:%s, out:%s" % (k, out) )
                continue

            #wlog("DEBUG, try_without:%s, ok" % k)

            # set without k
            headers_flag[k] = 0
            has_ok = True

        if has_ok:
            final_headers = {}
            for (sk, sv) in self.cand_headers.items():
                if headers_flag.get(sk, 0) == 1:
                    final_headers[sk] = sv;
            return final_headers

        return False

def check_from_file(url, must_contain, fname):
    headers = {}
    for line in open(fname):
        line = line.strip()
        if not line:
            continue
        arr = line.split(":", 1)
        if arr[0] == "":        # :authority: www.toutiao.com
            continue

        k = arr[0].strip()
        v = ""
        if len(arr) > 1:
            v = arr[1].strip()
        headers[k] = v

    dt = Detector(url, headers, must_contain)
    res = dt.run()
    if False == res:
        wlog("DETECT failed, url:%s, headers:%s, must_contain:%s" % (url, json.dumps(headers), must_contain))
        return

    print "====== useful headers ======="
    for (k,v) in res.items():
        print "%s: %s" % (k, v)
    print ""
 
def main():
    parser = argparse.ArgumentParser(description="AutoDetect useful http headers") 
    parser.add_argument("-u", "--url", help="url to check", required=True)
    parser.add_argument("-m", "--must_contain", help="to valid right http, response must contain these words", required=True)
    parser.add_argument("-f", "--file_headers", help="http headers to try", required=True)

    args = parser.parse_args()

    url = args.url
    must_contain = args.must_contain
    file_headers = args.file_headers

    check_from_file(url, must_contain, file_headers)

#
#
#
# ----------- DEBUG OR MAIN -----------------
#
if  __name__ == '__main__':
    main() 
#
# 

# -*- coding:utf-8 -*-
from os.path import abspath, dirname, join
import time
from bottle import route, request, run

save_dir = join(dirname(abspath(__file__)), "s_files")

save_raw_dir = join(dirname(abspath(__file__)), "s_raw_files")

@route('%s' % '/eventos', method='POST')
def do_upload():
    raw_data = request.body.read()
    raw_name = "raw_data_%s.txt" % time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
    with open(join(save_raw_dir, raw_name), "ab") as fp:
        fp.write(raw_data)

    data_list = raw_data.split(b"--myboundary\r\n")
    if data_list:
        for a_info in data_list:
            if b"Content-Type" in a_info:
                lines = a_info.split(b"\r\n")
                a_type = lines[0].split(b": ")[1]

                if a_type == b"image/jpeg":
                    a_name = "abc_%s.jpg" % time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
                    with open(join(save_dir, a_name), "wb") as fp:
                        data = b"\r\n".join(lines[3:-3])
                        fp.write(data)
                else:
                    a_name = "abc_%s.txt" % time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
                    with open(join(save_dir, a_name), "wb") as fp:
                        data = b"\r\n".join(lines[3:-1])
                        fp.write(data)
    return 'OK'


run(host='%s' % '192.168.1.100', port=3000, debug=True)

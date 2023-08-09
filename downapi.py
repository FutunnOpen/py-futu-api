import os
import os.path
import requests
import io
import traceback
import sys

openapi_web_url = 'http://10.1.133.107'
web_files_url = 'http://10.1.133.107:8081/files'
download_file_url = openapi_web_url + '/api/fs/download_file'
ls_url = openapi_web_url + '/api/fs/ls'

def get_exc_traceback_str():
    with io.StringIO() as strio:
        traceback.print_exc(file=strio)
        return strio.getvalue()

def http_download_file(remote_subpath, dst_dir, logger=None):
    rsp = None
    try:
        filename = os.path.split(remote_subpath)[1]
        rsp = requests.post(download_file_url, json={'filepath': remote_subpath})
        rsp.raise_for_status()
        if rsp.ok:
            with open(os.path.join(dst_dir, filename), 'wb') as f:
                for data in rsp.iter_content(1024*1024):
                    f.write(data)
            if logger:
                logger.info('Download http: from={}; to={};'.format(remote_subpath, dst_dir))
    except Exception:
        if logger:
            logger.warning('Download http err: from={}; to={}; http_code={}; http_msg={}; err={};'.format(
                remote_subpath, dst_dir, rsp.status_code, rsp.reason, get_exc_traceback_str()
            ))
        raise

def http_download_dir(local_dir: str, remote_dir: str, logger=None):
    remote_dir = remote_dir.lstrip('/\\')
    os.makedirs(local_dir, exist_ok=True)
    remote_items = http_list_dir(remote_dir, logger)
    for remote_item in remote_items:
        if remote_item['type'] == 'dir':
            remote_sub_dir = remote_dir + '/' + remote_item['name']
            local_sub_dir = os.path.join(local_dir, remote_item['name'])
            os.makedirs(local_sub_dir, exist_ok=True)
            http_download_dir(local_sub_dir, remote_sub_dir, logger)
        elif remote_item['type'] == 'file':
            http_download_file(remote_dir+'/'+remote_item['name'], local_dir, logger)


def http_list_dir(remote_dir: str, logger=None):
    remote_dir = remote_dir.lstrip('/\\')
    rsp = None
    try:
        rsp = requests.post(ls_url, json={'dir': remote_dir})
        rsp.raise_for_status()
        if rsp.ok:
            return rsp.json()['items']
        data = rsp.json()
        if data['err'] != 'OK':
            raise RuntimeError('Http ls err: {}'.format(data['err_msg']))
    except Exception:
        if logger:
            http_status_code, http_reason = '', ''
            if rsp:
                http_status_code, http_reason = rsp.status_code, rsp.reason
            if logger:
                logger.warning(
                    'Http ls err: from={}; remote_dir={}; http_code={}; http_msg={}; err={};'.format(ls_url,
                                                                                                     remote_dir,
                                                                                                     http_status_code,
                                                                                                     http_reason,
                                                                                                     get_exc_traceback_str()))
        raise


if __name__ == '__main__':
    remote_dir = 'http://10.1.133.107/files/build/FutuOpenD/7.3.3509/MM_7.3.3509_20230719101500/Update'
    local_dir = 'D:/MMUpdate'
    remote_dir = remote_dir.lstrip(web_files_url)
    http_download_dir(local_dir, remote_dir)

#!/usr/bin/python3

import requests
import json

class GNSTools:
    def __init__(self, ip='http://127.0.0.1:3080', auth = ('admin', 'admin')):
        self.ip = ip
        self.auth = auth
        self.sess = requests.Session()
        conn = self.sess.get(self.ip, auth=self.auth)
        if conn.status_code == 200:
            print('Succesfully connected to {}'.format(self.ip))
        else:
            print('Something went wrong...\nCode number: {}'.format(conn.status_code))
    def version(self):
        ver_url = self.ip + '/v2/version'
        version = (self.sess.get(ver_url, auth = self.auth)).json()
        return version
    def get_resource(self, resource=None):
        if resource == None:
            print('Select resource to view')
        else:
            resource = self.ip + '/v2/{}'.format(resource)
            req_res = self.sess.get(resource, auth = self.auth)
            print(req_res)
    def get_project(self, name='all'):
        url = self.ip + '/v2/projects'
        resource = self.sess.get(url, auth = self.auth)
        if name == 'all':
            return resource.json()
        else:
            for fname in resource.json():
                if fname['name'] == name:
                    url = self.ip + '/v2/projects/{}'.format(fname['project_id'])
                    resource = self.sess.get(url, auth=self.auth)
                    return resource.json()
    def get_nodes(self, prj_id, name='all'):
        url = self.ip + '/v2/projects/{}/nodes'.format(prj_id)
        resource = self.sess.get(url, auth=self.auth)
        if name == 'all':
            return resource.json()
        else:
            for node in resource.json():
                if node['name'] == name:
                    url = self.ip + '/v2/projects/{}/nodes/{}'.format(prj_id, node['node_id'])
                    resource = self.sess.get(url, auth=self.auth)
                    return resource.json()
    def create_project(self, name):
        url = self.ip + '/v2/projects'
        req = self.sess.post(url, auth=self.auth, data=json.dumps({'name': name}))
        return req.json()
    def delete_project(self, prj_id):
        url = self.ip + '/v2/projects/{}'.format(prj_id)
        req = self.sess.delete(url, auth=self.auth)
        return req
    def create_node(self, prj_id, name, node_type, compute='local'):
        url = self.ip + '/v2/projects/{}/nodes'.format(prj_id)
        req = self.sess.post(url, auth=self.auth, data=json.dumps({'name': name, 
                            'node_type': node_type, 'compute': compute}))
        return req.json()
    def delete_node(self, prj_id, node_id):
        url = self.ip + '/v2/projects/{}/nodes/{}'.format(prj_id, node_id)
        req = self.sess.delete(url, auth=self.auth)
        return req
    def reconfig_node(self, prj_id, node_id, params):
        url = self.ip + '/v2/projects/{}/nodes/{}'.format(prj_id, node_id)
        req = self.sess.put(url, auth=self.auth, data=json.dumps(params))
        return req.json()
    def connect_nodes(self, prj_id, node1, node2):
        dict_param = {"nodes": [node1, node2]}
        url = self.ip + '/v2/projects/{}/links'.format(prj_id)
        req = self.sess.post(url, auth=self.auth, data = json.dumps(dict_param))
        return req.json()
    def start_node(self, prj_id, node_id='all'):
        list_nodes = self.get_nodes(prj_id, name='all')
        if node_id == 'all':
            result_req = {}
            for n in list_nodes:
                url = self.ip + '/v2/projects/{}/nodes/{}/start'.format(prj_id, n['node_id'])
                req = self.sess.post(url, auth=self.auth)
                result_req[n['node_id']] = req.status_code
            return result_req
        else:
            url = self.ip + '/v2/projects/{}/nodes/{}/start'.format(prj_id, node_id)
            req = self.sess.post(url, auth = self.auth)
            return req.json()

    def stop_node(self, prj_id, node_id='all'):
        list_nodes = self.get_nodes(prj_id, name='all')
        if node_id == 'all':
            result_req = {}
            for n in list_nodes:
                url = self.ip + '/v2/projects/{}/nodes/{}/stop'.format(prj_id, n['node_id'])
                req = self.sess.post(url, auth=self.auth)
                result_req[n['node_id']] = req.status_code
            return result_req
        else:
            url = self.ip + '/v2/projects/{}/nodes/{}/stop'.format(prj_id, node_id)
            req = self.sess.post(url, auth = self.auth)
            return req.json()



if __name__ == '__main__':
    test = GNSTools()
    print(test.version())

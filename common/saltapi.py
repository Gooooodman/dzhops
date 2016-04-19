#coding=utf-8
 
import urllib2, urllib, json, re
 
class SaltAPI(object):
    def __init__(self,url,username,password):
        self.__url = url.rstrip('/')
        self.__user =  username
        self.__password = password
        self.__token_id = self.salt_login()
 
    def salt_login(self):
        params = {'eauth': 'pam', 'username': self.__user, 'password': self.__password}
        encode = urllib.urlencode(params)
        obj = urllib.unquote(encode)
        headers = {'X-Auth-Token':''}
        url = self.__url + '/login'
        req = urllib2.Request(url, obj, headers)
        opener = urllib2.urlopen(req)
        content = json.loads(opener.read())
        try:
            token = content['return'][0]['token']
            return token
        except KeyError:
            raise KeyError
 
    def postRequest(self, obj, prefix='/'):
        url = self.__url + prefix
        headers = {'X-Auth-Token'   : self.__token_id}
        req = urllib2.Request(url, obj, headers)
        opener = urllib2.urlopen(req)
        content = json.loads(opener.read())
        return content
        
    def list_all_key(self):
        '''
        [u'local', u'minions_rejected', u'minions_denied', u'minions_pre', u'minions']
        '''

        params = {'client': 'wheel', 'fun': 'key.list_all'}
        obj = urllib.urlencode(params)
        #self.salt_login()
        content = self.postRequest(obj)
        minions = content['return'][0]['data']['return']['minions']
        minions_pre = content['return'][0]['data']['return']['minions_pre']
        minions_rej = content['return'][0]['data']['return']['minions_rejected']
        return minions, minions_pre, minions_rej

    def delete_key(self,node_name):
        params = {'client': 'wheel', 'fun': 'key.delete', 'match': node_name}
        obj = urllib.urlencode(params)
        #self.salt_login()
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret

    def accept_key(self,node_name):
        params = {'client': 'wheel', 'fun': 'key.accept', 'match': node_name}
        obj = urllib.urlencode(params)
        #self.salt_login()
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret

    def remote_noarg_execution(self,tgt,fun):
        ''' Execute commands without parameters '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun}
        obj = urllib.urlencode(params)
        #self.salt_login()
        content = self.postRequest(obj)
        ret = content['return'][0][tgt]
        return ret

    def remote_execution(self,arg):
        ''' Command execution with parameters '''        
        params = {'client': 'local', 'tgt': '*', 'fun': 'cmd.run', 'arg': arg}
        obj = urllib.urlencode(params)
        #obj, number = re.subn("arg\d", 'arg', obj)
        #self.salt_login()
        content = self.postRequest(obj)
        ret = content['return'][0]
        return ret

    def list_remote_execution(self,tgt,arg):
        ''' Command execution with parameters '''
        params = {'client': 'local', 'tgt': tgt, 'fun': 'cmd.run', 'arg': arg, 'expr_form': 'list'}
        obj = urllib.urlencode(params)
        #obj, number = re.subn("arg\d", 'arg', obj)
        #self.salt_login()
        content = self.postRequest(obj)
        ret = content['return'][0]
        return ret

    def target_remote_execution(self,tgt,fun,arg):
        ''' Use targeting for remote execution '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': 'nodegroup'}
        obj = urllib.urlencode(params)
        #self.salt_login()
        content = self.postRequest(obj)
        jid = content['return'][0]['jid']
        return jid

    def deploy(self,tgt,arg):
        ''' Module deployment '''
        params = {'client': 'local', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg}
        obj = urllib.urlencode(params)
        #self.salt_login()
        content = self.postRequest(obj)
        return content

    def masterToMinion(self,tgt,fun,arg):
        '''

        '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg}
        obj = urllib.urlencode(params)
        #self.salt_login()
        content = self.postRequest(obj)
        return content

    def async_deploy(self,tgt,arg):
        '''
        Master对Minion异步执行sls文件；
        tgt 为目标minion组成的字符串，格式如 'zhaogb-201, zhaogb-202, zhaogb-203, ...'
        arg 为要使用的sls文件，如：dzh_sls.mobileserver.install
        返回值为salt jid，字符串，形如：'20160217132522942860'
        '''
        params = {'client': 'local_async', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg, 'expr_form': 'list'}
        obj = urllib.urlencode(params)
        #self.salt_login()
        content = self.postRequest(obj)
        jid = content['return'][0]['jid']
        return jid

    def async_deploy_all(self,arg):
        '''
        Master对所有Minion异步执行sls文件；因为是所有minion，所以无需传入目标主机，方法内直接写为'*';
        arg 为要使用的sls文件，如：dzh_sls.mobileserver.install
        返回值为salt jid，字符串，形如：'20160217132522942860'
        '''
        params = {'client': 'local_async', 'tgt': '*', 'fun': 'state.sls', 'arg': arg}
        obj = urllib.urlencode(params)
        #self.salt_login()
        content = self.postRequest(obj)
        jid = content['return'][0]['jid']
        return jid

    def async_deploy_fun(self, tgt, fun, arg):
        '''
            tgt is a list,for example 'zhaogb-201, zhaogb-202, zhaogb-203, ...'
        '''
        params = {'client': 'local_async', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': 'list'}
        obj = urllib.urlencode(params)
        #self.salt_login()
        content = self.postRequest(obj)
        jid = content['return'][0]['jid']
        return jid

    def masterToMinionContent(self, tgt, fun, arg):
        '''
            return Content, not jid;
            tgt is a list,for example 'zhaogb-201, zhaogb-202, zhaogb-203, ...'
        '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': 'list'}
        obj = urllib.urlencode(params)
        content = self.postRequest(obj)
        result = content['return'][0]
        return result


    def async_deploy_fun_all(self, fun, arg):
        '''
        Asynchronously send a command to connected minions
        tgt is a star,for example '*'
        '''
        params = {'client': 'local_async', 'tgt': '*', 'fun': fun, 'arg': arg}
        obj = urllib.urlencode(params)
        #self.salt_login()
        content = self.postRequest(obj)
        jid = content['return'][0]['jid']
        return jid

    def target_deploy(self,tgt,arg):
        ''' Based on the node group forms deployment '''
        params = {'client': 'local_async', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg, 'expr_form': 'nodegroup'}
        obj = urllib.urlencode(params)
        #self.salt_login()
        content = self.postRequest(obj)
        jid = content['return'][0]['jid']
        return jid

    def saltCmd(self, params):
        obj = urllib.urlencode(params)
#        obj, number = re.subn("arg\d", 'arg', obj)
        res = self.postRequest(obj)
        return res
 
def main():
    #以下是用来测试saltAPI类的部分
    #sapi = SaltAPI()
    #params = {'client':'local', 'fun':'test.ping', 'tgt':'*'}
    #params = {'client':'local', 'fun':'test.ping', 'tgt':'某台服务器的key'}
    #params = {'client':'local', 'fun':'test.echo', 'tgt':'某台服务器的key', 'arg1':'hello'}
    #params = {'client':'local', 'fun':'test.ping', 'tgt':'某组服务器的组名', 'expr_form':'nodegroup'}
    #params = {'client':'local', 'fun':'test.ping', 'tgt':'zhaogb-201, zhaogb-202, ...', 'expr_form':'list'}
    #test = sapi.saltCmd(params)
    #print test
    pass
 
if __name__ == '__main__':
    main()

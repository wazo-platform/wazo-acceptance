import web, os, sys
local_path = '/var/www/load-monitor/www/'
if local_path not in sys.path:
    sys.path.append(local_path)
import functions

os.chdir('/var/www/load-monitor/www/')
#web.header('Content-Type','text/html;charset=utf-8')

urls = (
'/.*', 'hello',
)

class hello:
    def GET(self):
        content = 'http://192.168.32.241/munin/lan-quebec.avencall.com/xivo-business.lan-quebec.avencall.com/'
        logs_sip_list = functions.list_sip_tests()
        tests_status = functions.get_tests_status(logs_sip_list[0])
        if tests_status == 'RUNNING':
            readed_log = functions.read_log_file(local_path + 'logs/sip_logs/' + logs_sip_list[0] )
        else:
            readed_log = 'N/A'
        render = web.template.render('templates', base='template_skeleton')
        return render.template_graphs("Load Monitor :: Graphs", content, tests_status, readed_log)

#application = web.application(urls, globals())
application = web.application(urls, globals()).wsgifunc()

"""
if __name__ == "__main__":
    application.run()
"""

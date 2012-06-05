import web, os, sys
local_path = '/var/www/load-monitor/'
if local_path not in sys.path:
    sys.path.append(local_path + 'www/')
import functions

os.chdir('/var/www/load-monitor/www/')
#web.header('Content-Type','text/html;charset=utf-8')

urls = (
'/.*', 'hello',
)

class hello:
    def GET(self):
        # lien pour trouver la page munin du server generant les graphs
        content = 'http://192.168.32.241/munin/lan-quebec.avencall.com/xivo-business.lan-quebec.avencall.com/'
        # liste des logs de sipp
        logs_sip_list = functions.list_sip_tests()
        # status d'un test en cours ou non : RUNNING ou NOT RUNNING
        # si un test est en cours, on veut afficher des stats en rapport
        tests_status = functions.get_tests_status(logs_sip_list[0])
        if tests_status == 'RUNNING':
            readed_log = functions.read_log_file(local_path + 'logs/sip_logs/' + logs_sip_list[0] )
        else:
            readed_log = 'N/A'
        # tests
        ###
        toto = functions.read_log_file(local_path + 'logs/sip_logs/' + logs_sip_list[0] )
        tata = toto[0][0]
        starting_time = toto[0][0]
        elapsed_time = toto[0][3]
        target_rate = toto[0][5]
        call_rate = toto[0][6]
        incoming_call = toto[0][8]
        outgoing_call = toto[0][10]
        total_call_created = toto[0][12]
        current_call = toto[0][13]
        successful_call = toto[0][14]
        failed_call = toto[0][16]
        call_length = toto[0][60]
        ###
        # appelle la creation de la page web
        render = web.template.render('templates', base='template_skeleton')
        return render.template_graphs("Load Monitor :: Graphs", content, tests_status, call_length)

#application = web.application(urls, globals())
application = web.application(urls, globals()).wsgifunc()

"""
if __name__ == "__main__":
    application.run()
"""

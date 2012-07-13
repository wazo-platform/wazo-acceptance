import web, os, sys
from web import form
local_path = '/var/www/load-monitor/'
if local_path not in sys.path:
    sys.path.append(local_path + 'www/')
import functions, conf

os.chdir('/var/www/load-monitor/www/')
#web.header('Content-Type','text/html;charset=utf-8')

urls = (
'/', 'index',
'/ServerSelect', 'ServerSelect',
)

global broken_robot, working_robot
broken_robot = 'robot-bleu.jpg'
working_robot = 'robot-vert.jpg'

render = web.template.render('templates/')

class index:
    def GET(self):
        raise web.redirect('/ServerSelect?server_select=%s' % conf.server_list[0]['name'])

class ServerSelect:
    def GET(self):
        # lecture depuis l'uri
        web_input = web.input()
        server_name = web_input.server_select
        # print 'DEBUG : server_name = %s ' % server_name
        # lien pour trouver la page munin du server generant les graphs
        for value in conf.server_list:
            if value['name'] == server_name:
                watcher_ip = value['watcher_ip']
        content = 'http://' + watcher_ip + '/munin/' + conf.domain + '/' + server_name + '.' + conf.domain
        # liste des logs de sipp
        logs_sip_list = functions.list_sip_tests(server_name)
        # status d'un test en cours ou non : RUNNING ou NOT RUNNING
        # si un test est en cours, on veut afficher des stats en rapport
        tests_status = functions.get_tests_status(logs_sip_list[0])
        # index des valeurs dans le fichier csv
        starting_time = 0
        elapsed_time = 3
        target_rate = 5
        call_rate = 6
        incoming_call = 8
        outgoing_call = 10
        total_call_created = 12
        current_call = 13
        successful_call = 14
        failed_call = 16
        call_length = 60
        if tests_status == 'RUNNING':
            readed_log = functions.read_log_file(local_path, server_name, logs_sip_list[0])
            test_stats = (readed_log[-1][current_call], readed_log[-1][total_call_created])
            img_file = working_robot
        else:
            readed_log = 'N/A'
            test_stats = ('N/A', 'N/A')
            img_file = broken_robot
        # formulaire
        # Creation du formulaire de selection du serveur a monitorer
        nb_conf_servers = len(conf.server_list)
        select_box = []
        for offset in range(0, nb_conf_servers):
            server = conf.server_list[offset]['name']
            select_box.append((server, server))
        form_select_server = form.Form(
            form.Dropdown('server_select', select_box),
            form.Button("submit", type="submit", description="Submit"),
            )
        form_server_select = ''.join([input.render() for input in form_select_server.inputs])
        # appelle la creation de la page web
        #render = web.template.render('templates', base='template_skeleton')
        header = render.template_header(server_name, test_stats, tests_status, img_file)
        left_menu = render.template_left(form_server_select)
        graphs =  render.template_graphs(content)
        return render.template_skeleton(unicode(header), unicode(left_menu), unicode(graphs))

#application = web.application(urls, globals())
application = web.application(urls, globals()).wsgifunc()

"""
if __name__ == "__main__":
    application.run()
"""

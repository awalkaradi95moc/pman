#!/usr/bin/env python3.5

'''

Send simple messages to pman server.

'''


# import  threading
import  argparse
from    _colors     import  Colors
import  crunner
import  time
import  sys
import  json
import  pprint

class Client():

    ''' Represents an example client. '''

    def __init__(self, **kwargs):
        # threading.Thread.__init__(self)

        self.str_cmd        = ""
        self.str_ip         = ""
        self.str_port       = ""
        self.str_msg        = ""
        self.str_testsuite  = ""
        self.str_protocol   = "http"
        self.str_auid       = "<auid>"
        self.str_jid        = "<jid>"
        self.loopStart      = 0
        self.loopEnd        = 0
        self.txpause        = 1
        self.pp             = pprint.PrettyPrinter(indent=4)
        self.b_man         = False
        self.str_man       = ''

        self.b_quiet        = False

        for key,val in kwargs.items():
            if key == 'cmd':        self.str_cmd        = val
            if key == 'msg':        self.str_msg        = val
            if key == 'ip':         self.str_ip         = val
            if key == 'port':       self.str_port       = val
            if key == 'auid':       self.str_auid       = val
            if key == 'jid':        self.str_jid        = val
            if key == 'txpause':    self.txpause        = int(val)
            if key == 'testsuite':  self.str_testsuite  = val
            if key == 'loopStart':  self.loopStart      = int(val)
            if key == 'loopEnd':    self.loopEnd        = int(val)
            if key == 'b_quiet':    self.b_quiet        = val
            if key == 'man':        self.str_man        = val

        if len(self.str_man):
            print(self.man(on = self.str_man))
            sys.exit(0)

        self.shell                      = crunner.crunner(verbosity=-1)
        self.shell.b_splitCompound      = True
        self.shell.b_showStdOut         = not self.b_quiet
        self.shell.b_showStdErr         = not self.b_quiet
        self.shell.b_echoCmd            = not self.b_quiet

        if not self.b_quiet:

            print(Colors.LIGHT_GREEN)
            print("""
            \t+---------------------------------+
            \t| Welcome to the pman client test |
            \t+---------------------------------+
            """)
            print(Colors.CYAN + """
            This program sends command payloads to a 'pman' process manager. A
            command is a typical bash command string to be executed and managed
            by pman.

            In addition, several control messages can also be sent to 'pman'. Typically
            these relate to the saving of the internal database.

            Several "canned" command payloads are available, and are triggered
            by an appropriate "--testsuite <type> [--loop <loop>]":

                --testsuite POST:
                Create <loop> instances of 'cmd'. Any instances in the <cmd> of
                C-style literals like '%d' are replaced by the current <loop>
                count. These cmds are then executed/managed by 'pman'.

                --testsuite GET_endInfo:
                --testsuite GET_cmd:
                --testsuite GET_<path>:
                GET first <loop> jobInfo packages and return the <path> in the
                jobInfo tree. This path should NOT start with '/'!

            """)

            print(Colors.WHITE + "\t\tWill transmit to: " + Colors.LIGHT_BLUE, end='')
            print('%s://%s:%s' % (self.str_protocol, self.str_ip, self.str_port))
            print(Colors.WHITE + "\t\tIter-transmit delay: " + Colors.LIGHT_BLUE, end='')
            print('%d second(s)' % (self.txpause))

    def man(self, **kwargs):
        """
        Print some man for each understood command
        """

        str_man     = 'commands'
        str_amount  = 'full'

        for k, v in kwargs.items():
            if k == 'on':       str_man     = v
            if k == 'amount':   str_amount  = v

        if str_man == 'commands':
            str_commands = Colors.CYAN + """
            The following commands are serviced by this script:
            """ + "\n" + \
            self.man_searchREST(description   =   "short")   + "\n" + \
            self.man_search(    description   =   "short")   + "\n" + \
            self.man_done(      description   =   "short")   + "\n" + \
            self.man_info(      description   =   "short")   + "\n" + \
            self.man_run(       description   =   "short")   + "\n" + \
            self.man_get(       description   =   "short") + "\n"

            return str_commands

        if str_man  == 'searchREST':    return self.man_searchREST( description  =   str_amount)
        if str_man  == 'search':        return self.man_search(     description  =   str_amount)
        if str_man  == 'info':          return self.man_info(       description  =   str_amount)
        if str_man  == 'done':          return self.man_done(       description  =   str_amount)
        if str_man  == 'run':           return self.man_run(        description  =   str_amount)
        if str_man  == 'get':           return self.man_get(        description  =   str_amount)

    def man_searchREST(self, **kwargs):
        """
        """

        b_fullDescription   = False
        str_description     = "full"

        for k,v in kwargs.items():
            if k == 'description':  str_description = v
        if str_description == "full":   b_fullDescription   = True

        str_manTxt =   Colors.LIGHT_CYAN        + \
                       "\t\t%-20s" % "searchREST"    + \
                       Colors.LIGHT_PURPLE      + \
                       "%-60s" % "Search for a target using an external client and REST calls." + \
                        Colors.NO_COLOUR

        if b_fullDescription:
            str_manTxt += """

                This searches for a target by first GETting a list of all jobs and then
                GETting each job in turn and parsing its internal fields for a match.
                Effectively, the "client" does the search.

                EXAMPLE:
                """ + Colors.LIGHT_GREEN + """
                ./pman_client.py --ip 192.168.1.189 --port 5010  --msg  \\
                    '{  "action": "searchREST",
                        "meta": {
                                    "key": "auid",
                                    "value": "rudolphpienaar"
                                }
                    }'
                """ + Colors.NO_COLOUR

        return str_manTxt

    def man_search(self, **kwargs):
        """
        """

        b_fullDescription   = False
        str_description     = "full"

        for k,v in kwargs.items():
            if k == 'description':  str_description = v
        if str_description == "full":   b_fullDescription   = True

        str_manTxt =   Colors.LIGHT_CYAN        + \
                       "\t\t%-20s" % "search"       + \
                       Colors.LIGHT_PURPLE      + \
                       "%-60s" % "Search for a target in a single call." + \
                       Colors.NO_COLOUR

        if b_fullDescription:
            str_manTxt += """

                This searches for a target in a single call by triggering
                an internal search. Effectively the "server" does the search.

                EXAMPLE:
                """ + Colors.LIGHT_GREEN + """
                ./pman_client.py --ip 192.168.1.189 --port 5010  --msg  \\
                    '{  "action": "search",
                        "meta": {
                                    "key": "auid",
                                    "value": "rudolphpienaar"
                                }
                    }'
                """ + Colors.NO_COLOUR

        return str_manTxt

    def man_info(self, **kwargs):
        """
        """

        b_fullDescription   = False
        str_description     = "full"

        for k,v in kwargs.items():
            if k == 'description':  str_description = v
        if str_description == "full":   b_fullDescription   = True

        str_manTxt =   Colors.LIGHT_CYAN        + \
                       "\t\t%-20s" % "info"     + \
                       Colors.LIGHT_PURPLE      + \
                       "%-60s" % "returns information on the current job info." + \
                       Colors.NO_COLOUR

        if b_fullDescription:
            str_manTxt += """

                This searches over the jobs space for a job matching the hit
                pattern and returns the startInfo and endInfo fields

                The hit pattern is specified by searching for a <key> in the
                job space that has value <value>

                EXAMPLE:
                """ + Colors.LIGHT_GREEN + """
                ./pman_client.py --ip 192.168.1.189 --port 5010  --msg  \\
                    '{  "action": "info",
                        "meta": {
                                    "key":      "jid",
                                    "value":    "<jid>-1"
                                }
                    }'
                """ + Colors.NO_COLOUR

        return str_manTxt

    def man_done(self, **kwargs):
        """
        """

        b_fullDescription   = False
        str_description     = "full"

        for k,v in kwargs.items():
            if k == 'description':  str_description = v
        if str_description == "full":   b_fullDescription   = True

        str_manTxt =   Colors.LIGHT_CYAN        + \
                       "\t\t%-20s" % "done"       + \
                       Colors.LIGHT_PURPLE      + \
                       "%-60s" % "returns information on whether the job is done." + \
                       Colors.NO_COLOUR

        if b_fullDescription:
            str_manTxt += """

                This searches over the jobs space for a job matching the hit
                pattern and returns the OR'd returncode of all per-job components.

                The hit pattern is specified by searching for a <key> in the
                job space that has value <value>

                EXAMPLE:
                """ + Colors.LIGHT_GREEN + """
                ./pman_client.py --ip 192.168.1.189 --port 5010  --msg  \\
                    '{  "action": "done",
                        "meta": {
                                    "key":      "jid",
                                    "value":    "<jid>-1"
                                }
                    }'
                """ + Colors.NO_COLOUR

        return str_manTxt

    def man_run(self, **kwargs):
        """
        """

        b_fullDescription   = False
        str_description     = "full"

        for k,v in kwargs.items():
            if k == 'description':  str_description = v
        if str_description == "full":   b_fullDescription   = True

        str_manTxt =   Colors.LIGHT_CYAN        + \
                       "\t\t%-20s" % "run"       + \
                       Colors.LIGHT_PURPLE      + \
                       "%-60s" % "runs a command with optional meta information." + \
                       Colors.NO_COLOUR

        if b_fullDescription:
            str_manTxt += """

                This runs an actual <cmd>, as well some passing some additional meta
                information.

                EXAMPLE:
                """ + Colors.LIGHT_GREEN + """
                ./pman_client.py --ip 192.168.1.189 --port 5010 --cmd "cal 7 1970" --msg  \\
                    '{  "action": "run",
                        "meta": {
                                    "auid":     "rudolphpienaar",
                                    "jid":      "<jid>-1"
                                }
                    }'
                """ + Colors.NO_COLOUR

        return str_manTxt

    def man_get(self, **kwargs):
        """
        """

        b_fullDescription   = False
        str_description     = "full"

        for k,v in kwargs.items():
            if k == 'description':  str_description = v
        if str_description == "full":   b_fullDescription   = True

        str_manTxt =   Colors.LIGHT_CYAN        + \
                       "\t\t%-20s" % "get"       + \
                       Colors.LIGHT_PURPLE      + \
                       "%-60s" % "gets a specific quantum of job information." + \
                       Colors.NO_COLOUR

        if b_fullDescription:
            str_manTxt += """

                This GETs information from the internal DB tree.

                The actual quantum of information is specfied in the "path"
                meta parameter, and must start with "/". Any valid element down the
                path from the root of this job in that DB job space can be
                retrieved, eg:

                        /_01/endInfo
                        /_01/start/0/startInfo/0/cmd
                        /_01/end/0/endInfo/0/stdout

                EXAMPLE:
                """ + Colors.LIGHT_GREEN + """
                ./pman_client.py --ip 192.168.1.189 --port 5010 --msg  \\
                    '{  "action": "get",
                        "meta": {
                                    "path":     "/_01/endInfo"
                                }
                    }'
                """ + Colors.NO_COLOUR

        return str_manTxt

    def shell_reset(self):
        """
        "resets" i.e. re-initializes the internal crunner shell
        :return:
        """
        self.shell                      = crunner.crunner(verbosity=-1)
        self.shell.b_splitCompound      = True
        self.shell.b_showStdOut         = not self.b_quiet
        self.shell.b_showStdErr         = not self.b_quiet
        self.shell.b_echoCmd            = not self.b_quiet

    def testsuite_handle(self, **kwargs):
        """
        Handle the test suites.
        """

        # First, process the <cmd> string for any special characters


        str_shellCmd    = ""
        b_tx            = False
        str_cmd         = self.str_cmd
        str_test        = "POST"
        str_suffix      = ""
        l_testsuite     = self.str_testsuite.split('_')
        if len(l_testsuite) == 2:
            [str_test, str_suffix]  = l_testsuite
        if len(l_testsuite) == 1:
            [str_test]  = l_testsuite

        for l in range(self.loopStart, self.loopEnd):
            b_tx        = False
            if "%d" in self.str_cmd:
                str_cmd = self.str_cmd.replace("%d", str(l))
            self.shell_reset()

            if str_test == "POST":
                #
                # POST <cmd>
                #
                str_shellCmd    = "http POST http://%s:%s/api/v1/cmd/ Content-Type:application/json Accept:application/json payload:='{\"exec\": {\"cmd\": \"%s\"}, \"action\":\"run\",\"meta\":{\"auid\":\"%s\", \"jid\":\"%s-%d\"}}'" \
                                        % (self.str_ip, self.str_port, str_cmd, self.str_auid, self.str_jid, l)
                b_tx            = True
            if str_test == "GET":
                #
                # GET <cmd>
                #
                str_shellCmd    = "http GET http://%s:%s/api/v1/_%d/%s Content-Type:application/json Accept:application/json" \
                                  % (self.str_ip, self.str_port, l, str_suffix)
                b_tx            = True

            if b_tx:
                print(Colors.LIGHT_BLUE)
                print("Sending...")

                d_ret   = self.shell.run(str_shellCmd)

                print(Colors.LIGHT_GREEN)
                print("Receiving...")
                json_stdout         = {}
                json_stderr         = {}
                json_returncode     = {}
                if len(d_ret["stdout"]):
                    json_stdout         = {"stdout": json.loads(d_ret["stdout"])}
                else:
                    json_stdout         = {"stdout": ""}
                if len(d_ret["stderr"]):
                    json_stderr         = {"stderr" :d_ret["stderr"]}
                else:
                    json_stderr         = {"stderr": ""}
                if len(str(d_ret["returncode"])):
                    json_returncode     = {"returncode": json.loads(str(d_ret["returncode"]))}
                else:
                    json_returncode     = {"returncode": ""}
                d_out   = {
                    "0":    json_stdout,
                    "1":    json_stderr,
                    "2":    json_returncode
                }
                print(json.dumps(d_out, indent = 4))
                print("\n")
                print(Colors.LIGHT_RED + "Pausing for %d second(s)..." % self.txpause)
                time.sleep(self.txpause)
                print("\n")

    def action_process(self, d_msg):
        """
        Process the "action" in d_msg
        """

        if d_msg['action'] == 'searchREST':
            d_params    = d_msg['meta']
            str_key     = d_params['key']
            str_value   = d_params['value']
            # First get list of all "jobs"
            self.shell_reset()
            str_shellCmd    = "http GET http://%s:%s/api/v1/ Content-Type:application/json Accept:application/json" \
                              % (self.str_ip, self.str_port)
            d_ret       = self.shell.run(str_shellCmd)
            json_stdout = json.loads(d_ret['stdout'])
            json_GET    = json_stdout['GET']
            l_keys      = json_GET.keys()

            for j in l_keys:
                self.shell_reset()
                str_shellCmd    = "http GET http://%s:%s/api/v1/%s/%s Content-Type:application/json Accept:application/json" \
                                  % (self.str_ip, self.str_port, j, str_key)
                d_ret       = self.shell.run(str_shellCmd)
                json_stdout = json.loads(d_ret['stdout'])
                json_val    = json_stdout['GET'][j][str_key]
                if json_val == str_value:
                    print(j)

        if d_msg['action'] == 'search':
            d_params        = d_msg['meta']
            str_key         = d_params['key']
            str_value       = d_params['value']
            str_shellCmd    = "http POST http://%s:%s/api/v1/cmd/ Content-Type:application/json Accept:application/json payload:='{\"action\":\"search\",\"meta\":{\"key\":\"%s\", \"value\":\"%s\"}}'" \
                              % (self.str_ip, self.str_port, str_key, str_value)
            d_ret           = self.shell.run(str_shellCmd)
            json_stdout     = json.loads(d_ret['stdout'])
            json_hits       = json_stdout['hits']
            print(json.dumps(json_stdout, indent=4))

        if d_msg['action'] == 'info':
            d_params        = d_msg['meta']
            str_key         = d_params['key']
            str_value       = d_params['value']
            str_shellCmd    = "http POST http://%s:%s/api/v1/cmd/ Content-Type:application/json Accept:application/json payload:='{\"action\":\"info\",\"meta\":{\"key\":\"%s\", \"value\":\"%s\"}}'" \
                              % (self.str_ip, self.str_port, str_key, str_value)
            d_ret           = self.shell.run(str_shellCmd)
            json_stdout     = json.loads(d_ret['stdout'])
            json_hits       = json_stdout['hits']
            print(json.dumps(json_stdout, indent=4))

        if d_msg['action'] == 'done':
            d_params        = d_msg['meta']
            str_key         = d_params['key']
            str_value       = d_params['value']
            str_shellCmd    = "http POST http://%s:%s/api/v1/cmd/ Content-Type:application/json Accept:application/json payload:='{\"action\":\"done\",\"meta\":{\"key\":\"%s\", \"value\":\"%s\"}}'" \
                              % (self.str_ip, self.str_port, str_key, str_value)
            d_ret           = self.shell.run(str_shellCmd)
            json_stdout     = json.loads(d_ret['stdout'])
            json_hits       = json_stdout['hits']
            print(json.dumps(json_stdout, indent=4))

        if d_msg['action'] == 'run' and len(self.str_cmd):
            d_meta          = d_msg['meta']
            str_meta        = json.dumps(d_meta)
            str_shellCmd    = "http POST http://%s:%s/api/v1/cmd/ Content-Type:application/json Accept:application/json payload:='{\"exec\": {\"cmd\": \"%s\"}, \"action\":\"run\",\"meta\":%s}'" \
                              % (self.str_ip, self.str_port, self.str_cmd, str_meta)
            d_ret       = self.shell.run(str_shellCmd)
            json_stdout = json.loads(d_ret['stdout'])
            print(json.dumps(json_stdout, indent=4))

        if d_msg['action'] == 'get':
            d_meta          = d_msg['meta']
            str_meta        = json.dumps(d_meta)
            str_path        = d_meta['path']
            str_shellCmd    = "http GET http://%s:%s/api/v1%s Content-Type:application/json Accept:application/json" \
                              % (self.str_ip, self.str_port, str_path)
            d_ret       = self.shell.run(str_shellCmd)
            json_stdout = json.loads(d_ret['stdout'])
            print(json.dumps(json_stdout, indent=4))

    def run(self):
        ''' Connects to server. Send message, poll for and print result to standard out. '''

        if len(self.str_testsuite):
            self.testsuite_handle()

        if len(self.str_msg):
            d_msg   = json.loads(self.str_msg)

            if 'action' in d_msg.keys():
                self.action_process(d_msg)

if __name__ == '__main__':

    parser  = argparse.ArgumentParser(description = 'simple client for talking to pman')

    parser.add_argument(
        '--cmd',
        action  = 'store',
        dest    = 'cmd',
        default = '',
        help    = 'Command to be managed by pman.'
    )
    parser.add_argument(
        '--msg',
        action  = 'store',
        dest    = 'msg',
        default = '',
        help    = 'Control signal to send to pman.'
    )
    parser.add_argument(
        '--ip',
        action  = 'store',
        dest    = 'ip',
        default = '127.0.0.1',
        help    = 'IP to connect.'
    )
    parser.add_argument(
        '--port',
        action  = 'store',
        dest    = 'port',
        default = '5010',
        help    = 'Port to use.'
    )
    parser.add_argument(
        '--jid',
        help    = 'job ID.',
        dest    = 'jid',
        action  = 'store',
        default = '<jid>'
    )
    parser.add_argument(
        '--auid',
        help    = 'apparent user id',
        dest    = 'auid',
        action  = 'store',
        default = '<aiud>'
    )
    parser.add_argument(
        '--txpause',
        help    = 'pause length between transmits',
        dest    = 'txpause',
        action  = 'store',
        default = '1'
    )
    parser.add_argument(
        '--testsuite',
        help    = 'internal test suite',
        dest    = 'testsuite',
        action  = 'store',
        default = ''
    )
    parser.add_argument(
        '--loopStart',
        help    = 'start internal testsuite loop at loopStart',
        dest    = 'loopStart',
        action  = 'store',
        default = '0'
    )
    parser.add_argument(
        '--loopEnd',
        help    = 'end internal testsuite loop at loopEnd',
        dest    = 'loopEnd',
        action  = 'store',
        default = '0'
    )
    parser.add_argument(
        '--quiet',
        help    = 'if specified, only echo JSON output from server response',
        dest    = 'b_quiet',
        action  = 'store_true',
        default = False
    )
    parser.add_argument(
        '--man',
        help    = 'request help',
        dest    = 'man',
        action  = 'store',
        default = ''
    )

    args    = parser.parse_args()
    client  = Client(
                        msg         = args.msg,
                        cmd         = args.cmd,
                        ip          = args.ip,
                        port        = args.port,
                        jid         = args.jid,
                        auid        = args.auid,
                        txpause     = args.txpause,
                        testsuite   = args.testsuite,
                        loopStart   = args.loopStart,
                        loopEnd     = args.loopEnd,
                        b_quiet     = args.b_quiet,
                        man         = args.man
                )
    client.run()
    sys.exit(0)
from flask import Flask, request
import os
from streamonitor.bot import Bot
import streamonitor.log as log
from streamonitor.manager import Manager

site_counts = {
    "StripChat": 0,
    "Chaturbate": 0,
    "其他站点": 0
}

class HTTPManager(Manager):
    def __init__(self, streamers):
        super().__init__(streamers)
        self.logger = log.Logger("manager")

    def run(self):
        app = Flask(__name__)

        def header():
            return """
            <link rel="icon" href="https://assets.strpst.com/assets/icons/mstile-70x70.png" type="image/x-icon">
            <style>
            .container {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                flex-direction: column;
            }
            table {
                border: 1px solid;
                border-collapse: collapse;
                margin-top: 20px;
                width: 100%;
                table-layout: fixed;
            }
            th, td {
                text-align: center;
                padding: 5px;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }
            th {
                cursor: pointer;
            }
            .table-container {
                max-height: 80vh;
                overflow-y: auto;
            }
            .search-container {
                display: flex;
                align-items: center;
                margin-bottom: 10px;
            }
            .search-container input[type="text"] {
                margin-left: 10px;
                padding: 5px;
                width: 200px;
            }
            </style>
            """

        def scripts():
            return """
                <script>
                function sortTable(n) {
                    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
                    table = document.getElementById("streamTable");
                    switching = true;
                    // 设置排序方向为升序
                    dir = "asc";
                    while (switching) {
                        switching = false;
                        rows = table.getElementsByTagName("tr");
                        for (i = 1; i < (rows.length - 1); i++) {
                            shouldSwitch = false;
                            x = rows[i].getElementsByTagName("td")[n];
                            y = rows[i + 1].getElementsByTagName("td")[n];
                            if (dir == "asc") {
                                if (n === 0 || n === 3) {
                                    if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                                        shouldSwitch = true;
                                        break;
                                    }
                                } else if (n === 1) {
                                    if (x.textContent.toLowerCase() > y.textContent.toLowerCase()) {
                                        shouldSwitch = true;
                                        break;
                                    }
                                } else if (n === 2 || n === 4) {
                                    if (x.innerHTML.toLowerCase() === "true" && y.innerHTML.toLowerCase() === "false") {
                                        shouldSwitch = true;
                                        break;
                                    }
                                }
                            } else if (dir == "desc") {
                                if (n === 0 || n === 3) {
                                    if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                                        shouldSwitch = true;
                                        break;
                                    }
                                } else if (n === 1) {
                                    if (x.textContent.toLowerCase() < y.textContent.toLowerCase()) {
                                        shouldSwitch = true;
                                        break;
                                    }
                                } else if (n === 2 || n === 4) {
                                    if (x.innerHTML.toLowerCase() === "false" && y.innerHTML.toLowerCase() === "true") {
                                        shouldSwitch = true;
                                        break;
                                    }
                                }
                            }
                        }
                        if (shouldSwitch) {
                            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                            switching = true;
                            switchcount++;
                        } else {
                            if (switchcount == 0 && dir == "asc") {
                                dir = "desc";
                                switching = true;
                            }
                        }
                    }
                }

                function searchTable() {
                    var input, filter, table, tr, td, i, txtValue;
                    input = document.getElementById("searchInput");
                    filter = input.value.toLowerCase();
                    table = document.getElementById("streamTable");
                    tr = table.getElementsByTagName("tr");
                    for (i = 1; i < tr.length; i++) {
                        td = tr[i].getElementsByTagName("td")[1];
                        if (td) {
                            txtValue = td.textContent || td.innerText;
                            if (txtValue.toLowerCase().indexOf(filter) > -1) {
                                tr[i].style.display = "";
                            } else {
                                tr[i].style.display = "none";
                            }
                        }
                    }
                }
                </script>
            """

        @app.route('/')
        def status():

            for streamer in self.streamers:
                if streamer.site == "StripChat":
                    site_counts["StripChat"] += 1
                elif streamer.site == "Chaturbate":
                    site_counts["Chaturbate"] += 1
                else:
                    site_counts["其他站点"] += 1

            output = """
            <html>
            <head>
            <title>Streamonitor Status</title>
            """ + header() + scripts() + """
            </head>
            <body>
            <div class="container">
            <h1>Streamonitor Status</h1>
            <div class="search-container">
                <h4>点击标题排序</h4>
                <input type="text" id="searchInput" onkeyup="searchTable()" placeholder="搜索用户名">
            </div>
            
            <div>站点数量统计：&nbsp;&nbsp;&nbsp; StripChat: {sc_count} &nbsp;&nbsp;&nbsp; Chaturbate: {cb_count} &nbsp;&nbsp;&nbsp; 其他: {other_count}</div>

            <br>
            <div class="table-container">
            <table id="streamTable">
            <tr>
            <th onclick="sortTable(0)"> Site </th>
            <th onclick="sortTable(1)"> Username </th>
            <th onclick="sortTable(2)"> Started </th>
            <th onclick="sortTable(3)"> TO SEE </th>
            <th onclick="sortTable(4)"> Status </th>
            </tr>""".format(sc_count=site_counts["StripChat"], cb_count=site_counts["Chaturbate"],
                       other_count=site_counts["其他站点"])

            for streamer in self.streamers:
                if streamer.status() == "Channel online":
                    TO_SEE = "去看直播"
                    if streamer.site == "StripChat":
                        stream_url = '<a href="https://zh.stripchat.com/{u}/" target="_blank">{tosee}</a>'.format(
                            u=streamer.username,
                            tosee=TO_SEE)
                    elif streamer.site == "Chaturbate":
                        stream_url = '<a href="https://chaturbate.com/{u}/" target="_blank">{tosee}</a>'.format(
                            u=streamer.username,
                            tosee=TO_SEE)
                    else:
                        stream_url = "<a>未部署播放地址</a>"
                else:
                    stream_url = "<a>看不了</a>"

                output += """
                    <tr>
                    <td>{s}</td>
                    <td><a href="/recordings?user={u}&site={s}">{u}</a></td>
                    <td>{r}</td>
                    <td> {stream_url} </td>
                    <td>{st}</td>
                    </tr>""".format(s=streamer.site, r=streamer.running,
                                    st=streamer.status(), u=streamer.username, stream_url=stream_url)
            output += "</table></div></div></body></html>"
            return output

        @app.route('/recordings')
        def recordings():
            output = """
            <html>
            <head>
            <title>Streamonitor Recordings</title>
            """ + header() + """
            </head>
            <body>
            <div class="container">
            """ + scripts() + """
            """
            streamer = self.getStreamer(request.args.get("user"), request.args.get("site"))
            output += "<p>Recordings of {u} [{s}]</p>".format(u=streamer.username, s=streamer.siteslug)
            try:
                temp = "<p>"
                for elem in os.listdir("./downloads/{u} [{s}]".format(u=streamer.username, s=streamer.siteslug)):
                    temp += elem + "<br>"
                if temp == "<p>":
                    output = "<p>No recordings</p>"
                else:
                    output += temp + "</p>"
            except:
                output += "<p>No recordings</p>"
            output += "</div></body></html>"
            return output

        app.run(host='0.0.0.0', port=5000)

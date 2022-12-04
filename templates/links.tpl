<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html>
        <head>
            <title>IPTV Web Server</title>
            <style type="text/css">
              html {background-color: #eee; font-family: arial;}
              body {background-color: #fff; border: 1px solid #ddd;
                    padding: 15px; margin: 15px}
              pre {background-color: #eee; border: 1px solid #ddd; padding: 5px;}
            </style>
        </head>
        <body>
            <center style="font-size:45px">{{title}}</center>
            <pre>
% for id, name in names:
 <a style="font-size:26px" href="{{id}}">{{name}}</a>
% end
            </pre>
        </body>
</html>
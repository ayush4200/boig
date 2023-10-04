from django.http import HttpResponse

def home(request):
    login_hint = "The default username is '<strong><i>admin</i></strong>' and the default password is '<strong><i>testpass</i></strong>'."
    headline = "Let's build some chatbots!"
    html = f"""
    <html>
    <head>
        <style>
            body {{
                background-color: #f0f0f0;
                font-family: Arial, sans-serif;
            }}
            .container {{
                width: 80%;
                margin: auto;
                text-align: center;
                padding-top: 5%;
            }}
            .hint {{
                background-color: #f6f8fa;
                color: #24292e;
                border-left: 6px solid #d0d0d0;
                padding: 15px;
                margin: 15px 0;
                border-radius: 4px;
                line-height: 1.5;
                display: inline-block;
            }}
            a {{
                display: inline-block;
                margin: 20px;
                padding: 15px 30px;
                background-color: #007BFF;
                color: white;
                text-decoration: none;
                border-radius: 4px;
                font-size: 20px;
            }}
            a:hover {{
                background-color: #0056b3;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{headline}</h1>
            <div class="hint">
                <p>{login_hint}</p>
            </div>
            <p>
                <a href="/api/docs">API Docs</a>
                <a href="/admin">Admin</a>
            </p>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

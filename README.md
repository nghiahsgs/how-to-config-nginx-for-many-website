# how-to-config-nginx-for-many-website
how to config nginx for many website (áp dụng cho tất cả các loại webserver có port run: nodejs + flask+ laravel)


## Step0: Create and run 2 app flask at port 3000 and 3001
```
from flask import Flask, request, render_template
from flask_cors import CORS

app = Flask(__name__,static_folder="/")
CORS(app)


@app.route('/', methods=['GET','POST'])
def index():
    if request.method=="GET":
        return {'res':'day la web 2'}
    else:
        name=request.json['name']
        return {'name':name}


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=3001)

```

## Step1: Go to list file config for nginx
```
cd /etc/nginx/sites-available
```

## Step2: Copy default config file
```
cp default site1.conf
cp default site2.conf
```
## Step3: Change content of site1 -> siteN.conf

### site1
```
vi site1.conf
```

```
server {
        listen 80;
        listen [::]:80;

        server_name site1.com;

        root /var/www/example.com;
        index index.html;

        location / {
                proxy_pass http://localhost:3000; #whatever port your app runs on
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;

        }

}
```
That config mean: site1.com point to localhost:3000


### site2
```
vi site2.conf
```

```
server {
        listen 80;
        listen [::]:80;

        server_name site2.com;

        root /var/www/example.com;
        index index.html;

        location / {
                proxy_pass http://localhost:3001; #whatever port your app runs on
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;

        }

}
```
That config mean: site2.com point to localhost:3001

## Step4: Check everything config is OK or not ?
```
sudo nginx -t
```


## Step5: Create symbolic link from site-available to site-enabled
```
sudo ln -s /etc/nginx/sites-available/site1.conf /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/site2.conf /etc/nginx/sites-enabled/
```

## Step6: Restart nginx
```
service nginx restart
```

## Step7: Open browser and go to url to see results
```
site1.com
site2.com
```

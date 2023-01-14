from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import requests

#  API key for map location
api_key = "ApGFvkq9ihvxDGSNm9zQiD7L40-wq_fknk2THLGHn5j5oB4t8gRiUh40DG8qcxd1"


class RequestHandler(BaseHTTPRequestHandler):
    def _send_response(self, message):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(message, "utf8"))

    def do_GET(self):
        #######################################################
        # Specify the location you want to look up
        location = 'Tbilisi'
        # Build the URL for the request
        url = f'http://dev.virtualearth.net/REST/v1/Locations?q={location}&key={api_key}'
        # Make the request
        response = requests.get(url)
        # Get the latitude and longitude from the response
        data = response.json()
        latitude = data['resourceSets'][0]['resources'][0]['point']['coordinates'][0]
        longitude = data['resourceSets'][0]['resources'][0]['point']['coordinates'][1]

        ##########################################################
        #latitude = 41.6908605241911                  # from FMB130
        #longitude = 45.8297119140625                # from FMB130 
        #speedLimit = latitude + longitude  #from Speed limit API
        speedLimit = 90 #from Speed limit API
        message = f"""
        <html>

        <head>
        <title>Font Awesome Icons</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <script src="https://kit.fontawesome.com/a076d05399.js" crossorigin="anonymous"></script>
        </head>
        

        <body style="background-color: #17181B;text-align: center;">
        <h1 style="color:#FFC101">TTM</h1> 
    


        <div style="display: flex;text-align: left;">
         
        <div style="flex: 1;background-color: 1D1E22;">
        <!-- <h1 style="text-align: center;>TTM"</h1> -->
      
        <p style="font-size:21px;color:#2488FF;">Current Position  <i class="fas fa-car" style="font-size:20px;color:#2488FF;"></i></p>
        
        <p  style="color:#FFC101" > Latitude:  {latitude} </p>
        <p  style="color:#FFC101" >  Longitude: {longitude} </p> 
        <p  style="color:#FFC101" > Speed Limit: {speedLimit} </p>
        <p  style="color:#FFC101" > DOUT1 Status: 0 </p> 

        <br>
        <br>
        <p style="color:#2488FF">History  <i class="far fa-clock" style="font-size:18px;color:#2488FF;"></i></p>
        
        <p  style="color:#F94931;font-size: 14px;" > FMB130 #1 -- DOUT = 1 , Speed = 430km/h, N = 1 , 19:03 / 31/01/2023  </p>  
        <p  style="color:#F94931;font-size: 14px;" > FMB130 #1 -- DOUT = 1 , Speed = 70km/h , N = 1 , 19:02 / 30/01/2023  </p> 
        <p  style="color:#F94931;font-size: 14px;" > FMB130 #1 -- DOUT = 1 , Speed = 110km/h , N = 1 , 19:01 /29/01/2023  </p> 
        <p  style="color:#F94931;font-size: 14px;" > FMB130 #1 -- DOUT = 1 , Speed = 90km/h , N = 1 , 19:00 / 28/01/2023  </p> 
        <p  style="color:#F94931;font-size: 14px;" > FMB130 #1 -- DOUT = 1 , Speed = 90km/h , N = 1 , 19:00 / 28/01/2023  </p> 
       



        </div>

        

        <div style="flex: 1;background-color: 17181B;">
        <div  style="text-align: right; padding: 0px 0;"> 
        <iframe width="800" height="500" frameborder="0" src="https://www.bing.com/maps/embed?h=500&w=800&cp=41.70942360123007~44.80198053878257&lvl=13.13057655742525&typ=d&sty=h&src=SHELL&FORM=MBEDV8" scrolling="no">
        </iframe>
       
        </div>
        </div>
        </div>


        </body>
        </html>
        """
        self._send_response(message)

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

run()

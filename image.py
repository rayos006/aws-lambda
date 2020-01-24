import json

# Add your own ALB url here. Dont forget the path!
ALB_URL = "http://lambda-front-1032409517.us-west-2.elb.amazonaws.com/calculate"
# Add your own S3 base url here
S3_URL = "https://ray1red-images.s3-us-west-2.amazonaws.com/"

def lambda_handler(event, context):
    # Build the response for the browser
    response = {
        "statusCode": 200,
        "statusDescription": "200 OK",
        "isBase64Encoded": False,
        "headers": {
            "Content-Type": "text/html; charset=utf-8"
        }
    }

    # HTML Example that will pull an image from s3 based
    # On query parameter
    # Also calls the rekognition lambda to analyze
    response['body'] = '''
    <html>
        <head>
            <title>Pics</title>
            <style>
                html, body {
                margin: 0; padding: 0;
                font-family: arial; font-weight: 700; font-size: 3em;
                text-align: center;
                }
                table {
                  font-family: arial, sans-serif;
                  border-collapse: collapse;
                  width: 100%;
                }
                td, th {
                  border: 1px solid #dddddd;
                  text-align: left;
                  padding: 8px;
                }
                tr:nth-child(even) {
                  background-color: #dddddd;
                }
                img {
                    transform:rotate(180deg);
                    -ms-transform:rotate(180deg); /* IE 9 */
                    -webkit-transform:rotate(180deg); /* Opera, Chrome, and Safari */
                }
            </style>
        </head>
        <body>
            <p>What's in an Image?</p>
            <img style="-webkit-user-select: none;margin: auto;cursor: zoom-in;" src="''' + S3_URL + event['queryStringParameters']['key'] + '''" width="500" height="333"> </img>
            <button type="button" onclick="loadDoc()">Analyze</button>
            <table id="demo">
            </table>
        </body>
        <script>
            function loadDoc() {
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    var labels = JSON.parse(this.responseText);
                    var table = document.getElementById("demo");
                    table.html = ""
                    for (i = 0; i < labels.length; i++) {
                        var row = table.insertRow(0);
                        var cell1 = row.insertCell(0);
                        var cell2 = row.insertCell(1);
                        cell1.innerHTML = labels[i]['Name'];
                        cell2.innerHTML = labels[i]['Confidence'] + "%";
                    }
                    var row = table.insertRow(0);
                    var cell1 = row.insertCell(0);
                    var cell2 = row.insertCell(1);
                    cell1.innerHTML = "Name";
                    cell2.innerHTML = "Confidence";
                }
            };
            xhttp.open("GET", "''' + ALB_URL + '''?key='''+ event['queryStringParameters']['key'] + '''", true);
            xhttp.send();
            }
            </script>
        
    </html>'''
    
    return response

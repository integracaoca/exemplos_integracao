var log = console.log;

console.log = function(){
    let ts = Date.now();
    let date_ob = new Date(ts);
    log.apply(console, [date_ob.toLocaleString()].concat(arguments));
};

var http = require('http');
var server = http.createServer ( function(request,response){

response.writeHead(200,{"Content-Type":"text\plain"});
if(request.method == "GET")
    {
        console.log('GET at ' + request.url)
        var body = ''
        request.on('data', function(data) {
            body += data
            //console.log('Partial body: ' + body)
        })
        request.on('end', function() {
            //console.log('header: ' + request.rawHeaders)
            
            var waitTill = new Date(new Date().getTime() + 4 * 1000);
            while(waitTill > new Date()){}
            console.log('Body: ' + body)
            response.end("OK")
        })
        
    }
else if(request.method == "POST")
    {
        //response.end("received POST request.");
        //console.log("received POST request: "+request.url + " ");
        console.log('POST at ' + request.url)
        var body = ''
        request.on('data', function(data) {
            body += data
            //console.log('Partial body: ' + body)
        })
        request.on('end', function() {
            //console.log('header: ' + request.rawHeaders)
            console.log('Body: ' + body)
            response.writeHead(200, {'Content-Type': 'application/json'})
            response.end(JSON.stringify({"message":"Acesso Liberado","code":200,"auth":"true"}))
        })
        
    }
else
    {
        response.end("Undefined request .");
    }
});

server.listen(3000);
console.log("Servidor Rodando na porta 3000");
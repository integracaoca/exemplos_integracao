const express = require('express');
const bodyParser = require('body-parser');
const app = express();
 
 
app.use(bodyParser.raw({ type: 'multipart/mixed' }));
 
app.post('/', (req, res) => {
let raw_data = req.body;
 
let data_list = raw_data.toString().split("--myboundary\r\n");
if (data_list) {
  for (let a_info of data_list) {
     if (a_info.includes("Content-Type")) {
     let lines = a_info.split("\r\n");
     let a_type = lines[0].split(": ")[1];
 
     if (a_type == "image/jpeg") {
        let data = Buffer.from(lines.slice(3, -3).join("\r\n"), 'base64');
     } else {
        let data =lines.slice(3, -1).join("\r\n");
        console.log(data);
     }
     }
  }
}
 
res.send('OK');
});
 
app.listen(3000, '192.168.3.14', () => {
console.log('Servidor ouvindo na porta 3000 e IP 192.168.3.14!');
});
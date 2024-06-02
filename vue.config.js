const fs = require('fs')

const mosquittoCA = fs.readFileSync('./rootCA.crt');

module.exports = {
    devServer: {
      https: {

        // key: fs.readFileSync('../../mobileAppCertificates/localhostIP.key'),
        // cert: fs.readFileSync('./localhostIP.crt'),
        // ca: fs.readFileSync('./rootCA.crt'),
        key: fs.readFileSync('./localhost.key'),
        cert: fs.readFileSync('./localhost.crt'),
        ca: fs.readFileSync('./localhost.crt'),
      }
    },

  }



  

     
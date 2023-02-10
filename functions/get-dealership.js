function main(params) {
  return new Promise(function (resolve, reject) {
    const { CloudantV1 } = require("@ibm-cloud/cloudant");
    const { IamAuthenticator } = require("ibm-cloud-sdk-core");
    const authenticator = new IamAuthenticator({
      apikey: "TWMzuQCBlAZWNi3nVXfmueobUg6i63n49xF8w7G0G7nG",
    });
    const cloudant = CloudantV1.newInstance({
      authenticator: authenticator,
    });
    cloudant.setServiceUrl("https://apikey-v2-axihl5yl8jvktabs644nvaqelgaoj686nssgc6c6q2:b4cfc6868bb69eff823f47ed58551c11@f7db7a2a-3352-4f21-82cb-aca6224ad74c-bluemix.cloudantnosqldb.appdomain.cloud");
    if (params.st) {
      // return dealership with this state
      cloudant
        .postFind({ db: "dealerships", selector: { st: params.st } })
        .then((result) => {
          let code = 200;
          if (result.result.docs.length == 0) {
            code = 404;
          }
          resolve({
            statusCode: code,
            headers: { "Content-Type": "application/json" },
            body: result.result.docs,
          });
        })
        .catch((err) => {
          reject(err);
        });
    } else if (params.dealerId) {
      id = parseInt(params.dealerId);
      // return dealership with this id
      cloudant
        .postFind({
          db: "dealerships",
          selector: {
            id: parseInt(params.dealerId),
          },
        })
        .then((result) => {
          let code = 200;
          if (result.result.docs.length == 0) {
            code = 404;
          }
          resolve({
            statusCode: code,
            headers: { "Content-Type": "application/json" },
            body: result.result.docs,
          });
        })
        .catch((err) => {
          reject(err);
        });
    } else {
      // return all documents
      cloudant
        .postAllDocs({ db: "dealerships", includeDocs: true })
        .then((result) => {
          let code = 200;
          if (result.result.rows.length == 0) {
            code = 404;
          }
          resolve({
            statusCode: code,
            headers: { "Content-Type": "application/json" },
            body: result.result.rows,
          });
        })
        .catch((err) => {
          reject(err);
        });
    }
  });
}

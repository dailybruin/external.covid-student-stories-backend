const mongoose = require("mongoose");

class MongoHandler {
  constructor() {
    this.client = mongoose.createConnection("mongodb://localhost:27017/covid", {
      useNewUrlParser: true,
    });
  }
}

module.exports = MongoHandler;

const Base = require('./base.js');

module.exports = class extends Base {
  async indexAction() {
    this.body = 'hello world!';
    const test = this.model('test'); // controller 里实例化模型
    const data = await test.select();
    console.log(this);
    return this.success(data);
  }

  async findAction() {
    const test = this.model('test'); // controller 里实例化模型
    const findData = await test.where({type: 'small'}).find();
    console.log(this);
    return this.success(findData);
  }

  async addAction() {
    const model = this.model('test');
    const insertId = await model.add({id: 3, type: 'large', score: 100});
    console.log(this);
    return this.success(insertId);
  }

  async updateAction() {
    const model = this.model('test');
    const smallData = await model.where({type: 'small'}).find();
    const affectedRows = await model.where({type: 'small'}).update({score: smallData.score - 1});
    console.log(this);
    return this.success(affectedRows);
  }

  async deleteAction() {
    const model = this.model('test');
    const affectedRows = await model.where({type: 'large'}).delete();
    console.log(this);
    return this.success(affectedRows);
  }
};

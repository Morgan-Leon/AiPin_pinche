const Base = require('./base.js');

module.exports = class extends Base {
  indexAction() {
    // return this.display();
  }

  async findAllAction() {
    const routeModel = this.model('route'); // controller 里实例化模型
    const findAllData = await routeModel.select();
    return this.success(findAllData);
  }
};

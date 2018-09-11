module.exports = class extends think.Model {

  get schema() {
    return {
      type: { // 字段名称
        type: 'varchar(10)',
        default: 'small'
      },
      create_time: {
        type: 'datetime',
        default: () => think.datetime() // default 为一个函数
      },
      score: {
        type: 'int',
        default: data => { // data 为添加/更新时的数据
          return data.grade * 1.5;
        }
      }
    }
  }
};

## 项目内容
- 实现整屏滚动
- 事件控制为滑轮事件和点击事件两种
## 核心原理
- 利用样式的样式权重不同，触发transition。
- animate()改变样式，产生动画
- 通过定时器实现函数节流来缓解高频触发的事件：mousewheel（鼠标滚轮事件））
## 项目示范:
![image](https://github.com/luola63702168/Full-screen-scrolling/blob/master/images/case.png)

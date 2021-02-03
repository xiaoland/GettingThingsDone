# NothingLeft: A time management system
- 自己画的LOGO：![NonthingLeft-Logo](https://github.com/xiaoland/NothingLeft/blob/docs/image/NothingLeft-Logo.png)
- NothingLeft是一个基于GTD理念的时间管理系统
- Other languages: 
  - [English](./README_en.md)

## 简介-Introduction

### 关于GTD-About GTD:
- - Getting Things Done is a kind of time management system which was proposed by David Allen. Usually, we abbreviate Getting Things Done as GTD.
- [Gtd-Introduction](./GTD.md)

### 设计-How it works
- 那么，这个项目是如何使用，或者说工作的呢
- **交互（前端）**
  - 首先，我们需要一个可视化的交互口以便用户操作，而这种可视化的交互口是可以有很多种实现方式的。在这里，我就对一些初级阶段需要实现的交互方式进行列举和说明
    - ***1、网页/WEB端***：不得不说，web工具真的是很好用，轻量简洁。我个人目前考虑使用flutter来实现，不过我还不会js，但我会努力的，有人愿意也可以联系我一起开发
    - ***2、DUEROS语音交互***：通过语音交互，你可以很方便的对inbox进行整理、分类、规划等等，而DUEROS的各种设备销量都很不错，其对第三方技能开发的支持也很友善，因此我会在DUEROS上做一个技能，然后用户可以连接到公用或自己的服务器来使用
    - ***3、xiaolan/wukong-robot语音交互***：xiaolan和wukong-robot都是运行在各种DIY设备上的语音交互机器人，但它们与DUEROS的区别就是其都由广大开发者制作的。而其中的xiaolan就是我做的一个，虽然没有wukong厉害，但我会加油的
- **后端**
  - 很明显，后端就是支持整个软件运行的部分，其重要性显而易见
  - 那么关于后端我是打算使用python来编写的（毕竟我python比较熟），而且用python做后端的软件也不少，就比如「Instagram」
  - 后端包括了「服务端」和「基本业务」
    - 服务端就是给DUEROS等更多的非自有前端（如WEB端就是自有前端）的一个接口，用户也可以根据自己的喜好，按照我们提供的API接口来开发自己喜欢的交互方式
    - 而基本业务就是最底层的部分了。基本业务其实就是完全配合GTD，再加上一些创新的实现
- 到这里，相信你已经对本项目有了一定的认识，如果您想要了解更多，请查看我们的[Wiki](https://nothingleftproject.github.io/NothingLeft/)

### 更多-More
- 其实，我们所拥有的只有空间和时间，有了他们，我们什么都可以做到。而这个系统就是为了更好地利用时间而诞生的。
- 这么多年来，这么多的GTD工具，有哪个是真正可以的呢？做到GTD，靠的不仅仅是工具，还有使用者的习惯，这才是最重要的
- 因此，帮助使用者养成习惯，才能实现这个目的。
- 当然，要让使用者养成习惯，不单单关乎其自身意志，还有GTD工具的好用性。如果这个工具反而弄得使用者情况越来越糟糕，那就简直了...
- 要好用，一个就是**stuff的输入**要方便，这一块，我们采用语音输入和web的多端可用优势来方便基本输入
  - 当然，不止这样。输入时也要简洁而完备，而不是花半天时间来选择日历/重要性等等。
  - 我们致力于只需要一句对该stuff的简单描述，就可以利用NLP技术分离出各种信息，在「分类」时，用户还可以继续调整
  - 当然，我们还根据用户使用习惯来个性化输入，通过在输入时给予一些tips来避免用户输入stuff时“断片"或者给予选项补充语句
  - 而且输入界面要简单清晰，输入完一个接着下一个，要流畅平滑
- stuff输入完成以后的**分类**也是极为重要的，在这个过程，将会把stuff初步理清并校准
  - 分类，最直观的方式就是拖拽分类。用户进入分类后，stuff则一条条呈现在顶端，然后让用户拖入对应的分类桶中，有新的分类就添加新的桶即可
  - 避免过多的点击操作，速度要快，有实时保存。分错了还可以撤回。
  - 添加新的分类要让用户仔细考虑“真的需要添加新的吗？看看是不是其实可以不用的”，这是因为过多的分类总是不大好的，一些人就会纠结在这个问题上而不能继续
  - 当然，还可以存在多重分类，如：不可行动/参考资料，用户点击分类桶即可进入分类桶中再详细分类
- 分类之后是**组织**，在这里，将会生成行动链(ActionChain)和项目(Project)，利用这些，我们来高效地完成任务
  - _行动链(ActionChain)_ 是next action串起来后的形式，通过行动链，我们可以直观地看到整个计划，知道做完以后该做什么。
    - 行动链不只是单纯地连接stuff，它还允许stuff之间存在更多关系，如：可以因为某一个stuff完成的状态来决定下一步应该做什么，不同的结果，不同的分支
    - 一个stuff可以同时属于行动链和项目，行动链也可以连接项目
  - _项目(Project)_ 与行动链最大的不同就是其允许包含非行动型的stuff，它是一个决策组，包含了资料和行动stuff以及更多的信息
    - 但请注意，项目不一定是将stuff和stuff弄起来形成一个决策组，它更多是一个stuff被「拆分」开的结果
    - 如：写一个关于家乡文化的调查报告，那么你就需要将其分为「设计计划」「搜集资料」「整理资料」「编写文稿和PPT」等细化出来的行动
    - 当然，这些拆分出来的行动还可以有先后关系，从而被行动链化。
    - 因此，我们提供「从stuff创建Project」「组织起多个stuff为Project」，而且被拆分开得行动我们则标记为stuff下的action，action也可以被行动链串起来
  - _下一步行动(NextAction)_ 将「可以行动」清单中的stuff一个个连接，就会标记好每个stuff的next action
  - 当然，系统会根据你的next action自动生成行动链
  - 没有说用户一定要弄项目什么的出来，这是为了满足更多的需求罢了。
  - 一般，组织也可以被理解为细化，只要细化你的stuff成action，系统也会自动生成更多东西的，一切从简，只要理清了你的stuff，就算达到目的了
- 补充一点，在**分类**或**组织**时，如果发现某个stuff可以在2mins以内现在被完成的话，马上去执行，不要管那么多！马上执行！然后标记「2mins done」即可
- 最后，维护整个GTD系统正常运转，也是养成习惯的最难的地方：**回顾**
  - 系统会定期生成报告，提醒用户来查看并理清自己一个周期内都做了什么，有什么要改进的
  - 回顾这个步骤包含了「查看报告」「自我报告」「自我反省」等一系列步骤
  - 而且还要方便用户在想到什么时记录下来，随时随地就可以通过悬浮按钮添加stuff，不遗漏任何灵感，为下一周期作计划
- 为了帮助用户养成GTD的习惯，我们将允许用户自定义通过各种有趣的方式来提醒到用户手上，他应该看看“有没有新的stuff啦”等等的
- 而且全面了解本系统的功能，给予一个有趣的引导是非常重要的
- 还有隐私性，迁移性，离线性；界面要简洁快速顺畅，操作要方便流畅清晰，各种信息一目了然，快速进入状态，避免发呆/断片等


## About

### 贡献者-Contributors
- Lan_zhijiang(我)

- 当然也欢迎大家来一起开发
  - DingTalk: 18680171381
  - Email: lanzhijiang@foxmail.com
  - Wechat：18680171381
  - QQ: 1481605673

### 使用-Usage
- 请查看本项目的[Wiki](https://nothingleftproject.github.io/NothingLeft/)

### 提交记录-Commit Log
- 基本完成了user的全部内容，配合数据库
- 基本完成了http服务器，接入了user的一部分内容
- 第一次测试后端，开始第一次调试——user部分
  - 添加了启动检查数据库
  - 修复了各种各样的bug
- 调试成功，完整的http实现，测试成功了login功能
- 添加了建议、理念等的信息收集处(./research)
- 完成了在centos系统上的启动调试
- 完成了logout/signup/login功能并且调试没有问题
- 完成了root初始化的调试，没有问题
- 修了一堆关于user操作的bug
- 调试并完成了user_delete
- 修复了一堆关于user_info_update的bug
- 调试修复pass了user_info_update
- 测试修复pass了user_info_get_all
- 测试修复pass了user_info_get_one_multi
- 测试修复pass了user_get_permissions
- 测试修复pass新修复的安全bug
- 修复了一些因账户不存在的bug
- 测试修复pass了user_write_permissions
- 测试修复pass了user_edit_permissions
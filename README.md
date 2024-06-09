# ja-netfilter-modified
## ja-netfilter介绍
ja-netfilter是由知了大佬开发的Java代理工具，可用于激活Jet Brains系软件。

> 这里解释一下它的名字：其中ja是指java agent，是一种jvm技术，这是该工具的核心；而为什么和网络没关系，却带上了netfilter后缀呢？这是历史原因：从commit记录来看，一开始url和dns两个plugin是内置的，后面做了插件系统后，这俩模块就被独立出去了，ja-netfilter也就跟netfilter没有关联了。

原文地址：[介绍一个”牛逼闪闪”开源库：ja-netfilter](https://zhile.io/2021/11/29/ja-netfilter-javaagent-lib.html)

项目开源地址：[ja-netfilter: A Java Instrumentation Framework](https://gitee.com/ja-netfilter/ja-netfilter)

## 修改说明
- 修改dns.conf，添加了jetbrains验证激活码服务器域名。
- 修改power.conf，添加特定激活码的验证配置。

## 使用说明

### 原有的方法

使用网上公开的激活码，再配合ja-netfilter可以做到**临时激活**，有时重新打开软件或隔一段时间打开就会弹出激活码失效的提示，此时要想重新临时激活，需要删除下面的两个目录：
```
%userprofile%\AppData\Local\JetBrains
%userprofile%\AppData\Roaming\JetBrains
```
然后重复之前的激活步骤即可，此处不做过多讲解。

### 改进的方法
为什么现有方法仅能做到临时激活呢？通过抓包，我发现JetBrains系软件在启动时会访问Amazon CloudFront，即亚马逊的CDN服务器，之后软件便会提示激活码无效。由此猜测该服务器大概率用于验证激活码是否有效（包括是否被滥用、是否被封禁）。 在参考MoYuno大佬对ja-netfilter原理讲解的文章后，我对原有ja-netfilter的配置进行了一些修改，以屏蔽访问验证服务器，达到永久激活。

1. 安装好某JetBrains系软件，不要激活。若之前激活过，请删除上文中提到的两个目录。
2. 下载本仓库中的所有文件，并解压放到自定义目录下。
3. 打开scripts目录，**Windows**用户推荐运行**install-current-user.vbs**，完成后会有弹窗提示；**Linux**用户运行**install.sh**。
4. 打开软件，选择Activation code激活方式，复制**Activation code.txt**中的激活码，完成激活。

## 写在最后

请支持正版软件，本教程仅供技术交流使用。

## 参考资料
- [ja-netfilter power插件原理](https://www.xuzhengtong.com/2022/07/25/ja-netfilter/ja-netfilter-plugins-power/) 
- [分析ja-netfilter如何破解jetbrains的IDE - 知乎](https://zhuanlan.zhihu.com/p/494706735?ssr_src=heifetz)


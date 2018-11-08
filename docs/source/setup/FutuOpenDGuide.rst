=================
FutuOpenD使用说明
=================

基本介绍
----------

  FutuOpenD运行于客户本机或服务器，接收API协议，中转协议到富途后台并将处理后的数据返回给协议请求连接。

  FutuOpenD程序暂时不提供安装程序，直接提供程序压缩包。压缩包内除了各平台的执行程序，还有带有默认FutuOpenD配置文件（FutuOpenD.xml），默认FutuHisData配置文件（FutuHistData.xml）以及程序打包数据（Appdata.dat）。
  
  FutuOpenD配置文件用于配置FutuOpenD程序启动参数，若不存在则程序无法正常启动。
  
  FutuHisData用于配置历史数据位置，若不存在则历史数据接口无法获取到数据。
  
  程序打包数据是程序需要用到的一些数据量较大的信息，打包数据减少启动下载该数据用时，若不存在则程序无法正常启动。

免责声明
---------
  已开户用户需要同意 `免责声明 <https://www.futunn.com/about/api-disclaimer/>`_ 才可以使用FutuOpenD。


登录参数使用优先级
----------------
  1.命令行证书登录
  
  2.命令行帐号密码密文登录
  
  3.命令行帐号密码明文登录
  
  4.配置文件证书登录
  
  5.配置文件帐号密码密文登录
  
  6.配置文件帐号密码明文登录

  
配置文件
---------

FutuOpenD配置
~~~~~~~~~~~~~~

  FutuOpenD启动配置文件使用XML格式，如下图所示：

  .. image:: ../_static/FTOpenDConfig.png

  **配置项：**
  
  ====================   ==================================================================================================   ===========================================
  键值                   说明						                                                                          是否可选配置项
  ====================   ==================================================================================================   ===========================================
  ip                     监听地址																			                  是，不设置则默认0.0.0.0	
  api_port               API协议接收端口                                                                                      是，可以命令行指定
  push_proto_type        API协议支持PB以及Json格式，PB：0，Json：1，推送类协议通过该配置决定包体格式                          是，不设置则默认Json格式
  qot_push_frequency     API订阅数据推送频率控制，单位毫秒，目前不包括K线和分时                                               是，不设置则不限制频率
  rsa_private_key        API协议RSA加密私钥（PKCS#1）文件绝对路径                                                             是，不设置则协议不加密
  telnet_port            远程操作命令监听端口                                                                                 是，不设置则启用远程命令
  login_account          登录帐号                                                                                             是，可以使用证书登录或命令行输入
  login_pwd              登录密码明文                                                                                         是，可以使用密文、证书登录或命令行输入
  login_pwd_md5          登录密码密文（32位MD5加密16进制），密文明文都存在情况下，只使用密文                                  是，可以使用明文、证书登录或命令行输入
  login_cert_file        证书文件绝对路径，除帐号密码外的另一种登录方式输入，若同时存在帐号密码登录配置项，只使用证书登录     是，可以使用帐号密码登录或命令行输入
  log_level              日志级别，可填no,debug,info,warning,error,fatal                                                      是，默认info级别
  ====================   ==================================================================================================   ===========================================

.. note::
  密文是明文经过32位MD5加密后用16进制表示的数据，搜索在线MD5加密（注意，通过第三方网站计算可能有记录撞库的风险）或下载MD5计算工具可计算得到。
  
  32位MD5密文如下图红框区域（e10adc3949ba59abbe56e057f20f883e）：
  
  .. image:: ../_static/MD5.png

  FutuOpenD默认读取同目录下的FutuOpenD.xml。在MacOS上，由于系统保护机制，FutuOpenD.app在运行时会被分配一个随机路径，导致无法找到原本的路径。此时有以下方法：

  1. 执行tar包下的fixrun.sh
  2. 用命令行参数-cfg_file指定配置文件路径，见下面说明
 
  
RSA私钥文件
~~~~~~~~~~~~~~
  
 参考文件格式：
  
 .. code-block:: bash

		-----BEGIN RSA PRIVATE KEY-----
	MIICXAIBAAKBgQCx3W78hx5dQxg47hGMEj02JAJYP+HdKGWD8QilzeK4eL6QJ9QP
	+uVYGA5Jp0Ed2AaV+zQrT/BCe6z5j/Qd5B0eY2cFlgk+/hbAt7A4wcSAbby8nONw
	0fZTglU78FhLUih84Int5HO0Fr3WLUDvpE+TgS3l/2u5ym6H6fvsdrdNCwIDAQAB
	AoGAHep/s2vKmKcjWNf6DZQ3xXZzCoLcK4WS5YlSCglCHAL7EmYQjguGLbYGGS9P
	jYR7Pxi8YpiUcao5otQqnCh1GRFouU397D3h+bf/bQXINZcv3sxKFrXm9MNVaBJD
	W4BcC3HGfnlaIVTKU+qGkeA1BydP5AQyxsGOq00IUeGK4uECQQD/5xHLDwhwYFyc
	MK4xMnlrvne8TSlPBciWfrxQ7V/X0eP/HQ20VkVxc0tFD91aLrCap6OYcNV9jwJN
	wTQLt5wbAkEAse7C75LKW0+cMcROvAR3qLV2LbGjLW+cH6WmEP9CEGxi0aJg4Gs3
	oSRYfaC/RLI87sSb0DC5+mTswXduLGpB0QJAJk0ec6cHW1KA6fu7Rq/ITqEOaMef
	xC0YbbYAV5h/vNy0ZE2j7HbxI97eyDJsrf/I/QzURo+01HsgHCUrtglAOwJBAKiW
	cA7sh1zS5kxlErCkjvfDz1BmIhT3zfZSTjGGmYLUHyE/eAjKra+5rzqA5xjgxEj6
	8iLlOCFeJND+Jt5gYzECQH+HtFilF1SxGS4AHrJomHaMhk/IazjtUnLuFM/DuZ/h
	sxTqXpBBCtTqcAotMlx4ZJQYL3f2PmI2Q/o0NUMt40w=
	-----END RSA PRIVATE KEY-----
	
 .. note::

  * RSA 密钥的填充方式为 PKCS1, 位数1024
  * 密钥文件可通过第三方web平台自动生成， 请在baidu或google上搜索"RSA 在线生成"
  * 将私钥保存成文件，并在将文件路径配置在FutuOpenD.xml的rsa_private_key配置项
  * 公钥可通过私钥计算得到，但生成私钥时不要设置密码
  
  
FutuHistData配置
~~~~~~~~~~~~~~~~~

  历史数据下载启动配置文件使用XML格式，如下图所示：
  
  .. image:: ../_static/FTHistDataConfig.png
  
  **配置项：**
  
  =================   =============================================================================================================
  键值                说明						                                                             
  =================   =============================================================================================================
  enable              是否启用下载工具		
  nnid				  指定用于下载历史数据的牛牛号，需要先在FueuOpenD中登录该牛牛号，才能下载历史数据  
  begin_time          下载起始时间，时间格式为HHMM，每天到当地这个时间点开始下载                            
  end_time            下载结束时间，时间格式为HHMM，每天到当地这个时间点暂停下载，end小于start时表示end为第二天
  market              下载数据市场，可选市场类型为hk、us、cn，多个市用|连接，如hk|cn|us                  
  kline_type          下载K线数据类型，可选的K线类型为day、week、month、year、min1、min5、min15、min30、min60，多个类型用|连接                                                               
  hist_data_dir       历史数据存放位置绝对路径,修改后重启程序才生效	                                                                           
  =================   =============================================================================================================
  
---------------

启动命令行参数
---------------

  命令行部分参数与配置文件相同，同样参数若存在于命令行与配置文件，使用命令行参数。
  
  .. image:: ../_static/login-command.png
  
  传参格式：-key=value
  
  例如FutuOpenD.exe -login_account=100000 -login_pwd=123456 -lang=en

  
  **参数项：**
  
  ========================   ==================================================================================================   ================================================
  键值                       说明						                                                                          是否可选配置项
  ========================   ==================================================================================================   ================================================
  login_account              登录帐号																		                      是，可以使用证书登录或配置文件配置项
  login_pwd                  登录密码明文                                                                                         是，可以使用证书登录或配置文件配置项
  login_pwd_md5              登录密码密文（32位MD5加密16进制），密文明文都存在情况下，只使用密文                                  是，可以使用密文、证书登录或配置文件配置项
  login_cert_file            证书文件绝对路径，除帐号密码外的另一种登录方式输入，若同时存在帐号密码登录配置项，只使用证书登录     是，可以使用明文、证书登录或配置文件配置项   
  login_region               优先连接点区域，但不一定能连接上该区域连接点(gz/sh/hk)                                               是，不设置则自动选择
  cfg_file                   FutuOpenD配置文件绝对路径                                                                            是，不设置则使用程序所在目录下的FutuOpenD.xml
  hist_data_cfg_file         FutuHistData配置文件绝对路径 	                                                                      是，不设置则使用程序所在目录下的FutuHistData.xml
  console                    是否显示控制台，后台运行：0，控制台运行：1                                                           是，不设置则默认控制台运行
  lang						 FutuOpenD语言，en：英文，chs：简体中文                                                               是，不设置则默认简体中文
  api_port                   API协议接收端口                                                                                      是，不设置则使用配置文件配置项
  help                       输出启动命令行参数然后退出程序                                                                       是，不设置则正常启动FutuOpenD
  log_level                  日志级别，可填no,debug,info,warning,error,fatal                                                      是，默认info级别
  ========================   ==================================================================================================   ================================================

--------------

运维命令
--------------
  
  通过命令行或者Telent发送命令可以对FutuOpenD做运维操作。
  
  命令格式：**cmd -param_key1=param_value1 -param_key2=param_value2**
  
exit - 退出程序
~~~~~~~~~~~~~~~~

  exit 

  退出FutuOpenD程序


req_phone_verify_code - 请求手机验证码
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  req_phone_verify_code 

  请求手机验证码，当启用设备锁并初次在该设备登录，要求做安全验证。
  
input_phone_verify_code - 输入手机验证码
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  input_phone_verify_code -code=123456

  输入手机验证码，并继续登录流程。

  **Parameters: code** - str，手机验证码
 
req_pic_verify_code - 请求图形验证码
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  req_pic_verify_code 

  请求图形验证码，当多次输入错登录密码时，需要输入图形验证码。
  
input_pic_verify_code - 输入图形验证码
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  input_pic_verify_code -code=1234

  输入图形验证码，并继续登录流程。

  **Paramters code:** str，图形验证码
  
relogin - 重登录
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  relogin -login_pwd=123456

  当登录密码修改或中途打开设备锁等情况，要求用户重新登录时，可以使用该命令。只能重登当前帐号，不支持切换帐号。
  密码参数主要用于登录密码修改的情况，不指定密码则使用启动时登录密码。

  **Paramters login_pwd:** str，登录密码明文
  
  **Paramters login_pwd_md5:** str，登录密码密文（32位MD5加密16进制）
	  
help - 命令帮助
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  help -cmd=exit

  查看指定命令详细信息，不指定参数则输出命令列表

  **Paramters cmd:** str，命令
  
.. note::

    * 运维代码在Telnet窗口或命令控制台输入
    .. image:: ../_static/req-verify.png

1. 创建VPC，设置安全组，设置安全规则。（安全的虚拟云网络，做网络隔离，类似自己机房有自己单独的网络，防止外部直接访问内网，内部网络只通过ALB对外暴露端口，增加安全性）
2.新建EC2服务器，选择对应的配置。设置对应的Security Groups，允许ssh访问，
检查安全组（Security Group）：
入站规则（Inbound Rules）

必须包含 允许端口 22（SSH）访问

Source 设置为 0.0.0.0/0（或你的公网 IP）

如果 0.0.0.0/0 不安全，可以查找你的公网 IP：

curl ifconfig.me
然后在 AWS 安全组里添加规则，允许你的 IP 访问 端口 22。

3.通过本地ssh连接到ec2 服务器。
 a.EC2设置Key Pairs： 
   本地下载到一个.pem 文件，移动到/Users/mark/.ssh， 修改权限 chmod 400 
 b.生成公钥： ssh-keygen -y -f ~/.ssh/myec2.pem， 将公钥存入服务端 ~/.ssh/authorized_keys， 修改权限chmod 600 ~/.ssh/authorized_keys
 c. ssh登录ec2: ssh -i ~/.ssh/myec2.pem ec2-user@xxx.com

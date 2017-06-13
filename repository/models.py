from django.db import models


class UserProfile(models.Model):
    """
    用户信息
    """
    name = models.CharField(verbose_name='姓名',max_length=32)
    email = models.EmailField(verbose_name='邮箱')
    phone = models.CharField(verbose_name='座机',max_length=32,null=True,blank=True)
    mobile = models.CharField(verbose_name='手机',max_length=32)

    class Meta:
        verbose_name_plural = '用户表'
        db_table = 'userProfile'

    def __str__(self):
        return self.name

class AdminInfo(models.Model):
    """
    用户登陆相关信息
    """
    # 用户登陆和用户信息是一对一关心
    user_info = models.OneToOneField('UserProfile')
    username = models.CharField(verbose_name='用户名',max_length=64)
    password = models.CharField(verbose_name='密码',max_length=64)

    class Meta:
        db_table = 'adminInfo'
        verbose_name_plural = '管理员表'

    def __str__(self):
        return self.user_info.name

class UserGroup(models.Model):
    """
    用户组
    用户组和用户是多对多关系
    """
    # 组名唯一
    name = models.CharField(verbose_name='用户组',max_length=32,unique=True)
    user = models.ManyToManyField('UserProfile')

    class Meta:
        db_table = 'userGroup'
        verbose_name_plural = '用户组表'

    def __str__(self):
        return self.name

class BusinessUnit(models.Model):
    """
    业务线 -- 唯一
    一个用户组可能有多个业务线,里面有联系人和管理员
    """
    name = models.CharField(verbose_name='业务线',max_length=64,unique=True)
    contact = models.ForeignKey('UserGroup',verbose_name='业务联系人',related_name='c')
    manager = models.ForeignKey('UserGroup',verbose_name='系统管理员',related_name='m')

    class Meta:
        db_table = 'businessUnit'
        verbose_name_plural = '业务线表'

    def __str__(self):
        return self.name

class IDC(models.Model):
    """
    机房信息
    """
    name = models.CharField(verbose_name='机房',max_length=32)
    floor = models.IntegerField(verbose_name='楼层',default=1)

    class Meta:
        db_table = 'IDC'
        verbose_name_plural = '机房表'

    def __str__(self):
        return self.name

class Tag(models.Model):
    """
    资产标签
    """
    name = models.CharField(verbose_name='标签',max_length=32,unique=True)

    class Meta:
        db_table = 'tag'
        verbose_name_plural = '标签表'

    def __str__(self):
        return self.name

class Asset(models.Model):
    """
    资产信息表,所有资产公共信息(交换机,服务器,防火墙等)
    """
    device_type_choices = (
        (1,'服务器'),
        (2,'交换机'),
        (3,'防火墙'),
    )

    device_status_choices = (
        (1,'上架'),
        (2,'在线'),
        (3,'离线'),
        (4,'下架'),
    )

    device_type_id = models.IntegerField(verbose_name='资产类型',choices=device_type_choices,default=1)
    device_status_id = models.IntegerField(verbose_name='资产状态',choices=device_status_choices,default=1)

    cabinet_num = models.CharField(verbose_name='机柜号',max_length=30,null=True,blank=True)
    cabinet_order = models.CharField(verbose_name='机柜中序号',max_length=30,null=True,blank=True)

    idc = models.ForeignKey('IDC',verbose_name='IDC机房',null=True,blank=True)
    business_unit = models.ForeignKey('BusinessUnit',verbose_name='属于的业务线',null=True,blank=True)

    tag = models.ManyToManyField('Tag')

    # 最近更新时间
    latest_date = models.DateTimeField(null=True,blank=True)
    # 创建时间
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'asset'
        verbose_name_plural = '资产表'

    def __str__(self):
        return '%s-%s-%s' % (self.idc.name,self.cabinet_num,self.cabinet_order)

class Server(models.Model):
    """
    服务器信息
    """
    asset = models.OneToOneField('Asset')

    hostname = models.CharField(verbose_name='主机名',max_length=128,unique=True)

    # 为sn创建索引 快速查找
    sn = models.CharField(verbose_name='SN号',max_length=64,db_index=True)
    manufacturer = models.CharField(verbose_name='制造商',max_length=64,null=True,blank=True)
    model = models.CharField(verbose_name='型号',max_length=64,null=True,blank=True)

    manage_ip = models.GenericIPAddressField(verbose_name='管理IP',null=True,blank=True)
    os_platform = models.CharField(verbose_name='系统',max_length=16,null=True,blank=True)
    os_version = models.CharField(verbose_name='系统版本',max_length=16,null=True,blank=True)

    cpu_count = models.IntegerField(verbose_name='cpu个数',null=True,blank=True)
    cpu_physical_count = models.IntegerField(verbose_name='cpu物理个数',null=True,blank=True)
    cpu_model = models.CharField(verbose_name='cpu型号',max_length=128,null=True,blank=True)

    create_at = models.DateTimeField(auto_now_add=True,blank=True)

    class Meta:
        db_table = 'server'
        verbose_name_plural = '服务器表'

    def __str__(self):
        return self.hostname

class NetworkDevice(models.Model):
    """
    网络设备
    """
    asset = models.OneToOneField('Asset')
    management_ip = models.GenericIPAddressField(verbose_name='管理ip',max_length=64,blank=True,null=True)
    vlan_ip = models.GenericIPAddressField(verbose_name='VlanIP',max_length=64,blank=True,null=True)
    intranet_ip = models.GenericIPAddressField(verbose_name='内网ip',max_length=128,blank=True,null=True)
    sn = models.CharField(verbose_name='SN号',max_length=64,unique=True)
    manufacture = models.CharField(verbose_name='制造商',max_length=128,null=True,blank=True)
    model = models.CharField(verbose_name='型号',max_length=128,null=True,blank=True)
    port_num = models.SmallIntegerField(verbose_name='端口个数',null=True,blank=True)
    device_detail = models.CharField(verbose_name='设置详细配置',max_length=255,null=True,blank=True)

    class Meta:
        db_table = 'networkDevice'
        verbose_name_plural = '网络设备'

    def __str__(self):
        return '%s-%s-%s' % (self.sn,self.manufacture,self.model)

class Disk(models.Model):
    """
    硬盘信息
    """
    slot = models.CharField(verbose_name='插槽位',max_length=8)
    model = models.CharField(verbose_name='磁盘型号',max_length=32)
    capacity = models.FloatField(verbose_name='磁盘容量GB')
    pd_type = models.CharField(verbose_name='磁盘类型',max_length=32)
    server_obj = models.ForeignKey('Server',related_name='disk')

    class Meta:
        db_table = 'disk'
        verbose_name_plural = '硬盘表'

    def __str__(self):
        return '%s-%s-%s' % (self.slot, self.capacity, self.model)

class NIC(models.Model):
    """
    网卡信息
    """
    name = models.CharField(verbose_name='网卡名称',max_length=128)
    hwaddr = models.CharField(verbose_name='网卡mac地址',max_length=64)
    netmask = models.CharField(verbose_name='子网掩码',max_length=64)
    ipaddrs = models.CharField(verbose_name='ip地址',max_length=256)
    up = models.BooleanField(default=False)
    server_obj = models.ForeignKey('Server',related_name='nic')

    class Meta:
        db_table = 'nic'
        verbose_name_plural = '网卡表'

    def __str__(self):
        return self.name

class Memory(models.Model):
    """
    内存信息
    """
    slot = models.CharField(verbose_name='插槽位',max_length=32)
    manufacture = models.CharField(verbose_name='制造商',max_length=32,null=True,blank=True)
    model = models.CharField(verbose_name='型号',max_length=64)
    capacity = models.FloatField(verbose_name='容量',null=True,blank=True)
    sn = models.CharField(verbose_name='内存SN号',max_length=64,null=True,blank=True)
    speed = models.CharField(verbose_name='速度',max_length=16,null=True,blank=True)

    server_obj = models.ForeignKey('Server',related_name='memory')

    class Meta:
        db_table = 'memory'
        verbose_name_plural = '内存表'

    def __str__(self):
        return '%s-%s-%s' % (self.slot,self.capacity,self.sn)


class AssetRecord(models.Model):
    """
    资产变更记录,createor为空时,表示是资产汇报的数据
    """
    asset_obj = models.ForeignKey('Asset',related_name='ar')
    content = models.TextField(verbose_name='数据详情',null=True,blank=True)
    creator = models.ForeignKey('UserProfile',null=True,blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'assetRecord'
        verbose_name_plural = '资产记录表'

    def __str__(self):
        return '%s-%s-%s' % (self.asset_obj.idc.name,self.asset_obj.cabinet_num,self.asset_obj.cabinet_order)

class ErrorLog(models.Model):
    """
    错我日志,如agent采集数据错误 或运行错误
    """
    asset_obj = models.ForeignKey('Asset',null=True,blank=True)
    title = models.CharField(verbose_name='错误标题',max_length=16)
    content = models.TextField(verbose_name='错误信息')
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'errorLog'
        verbose_name_plural = '错误日志表'

    def __str__(self):
        return self.title
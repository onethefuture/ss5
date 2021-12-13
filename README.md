# ss5-
自建ss5二进制包
本机环境：Centos7

1、首先安装rpmbuild工具和编译环境
#yum –y install rpmdevtools
#yum -y install gcc automake make pam-devel openldap-devel cyrus-sasl-devel openssl-devel

2、执行如下rpmdev-setuptree生成rpmbuild的工作目录(会在当前用户的根目录生成rpmbuild目录)
#rpmdev-setuptree

3、查看生成的rpmbuid工作目录
[root@master ~]# tree
.
├── anaconda-ks.cfg
└── rpmbuild
    ├── BUILD        #打包过程中的工作目录
    ├── RPMS		#存放生成的二进制包
    ├── SOURCES    #放置打包资源，包括源码打包文件和补丁文件
    ├── SPECS		#放置SPEC文档
    └── SRPMS		#存放生成的源码包

6 directories, 1 file

4、.spec
若要构建一个标准的RPM包，需要构建.spec文件,其中包含打包的全部信息。然后，对此文件执行rpmbuild命令
1>撰写SPEC文件
SPEC撰写是打包RPM的核心

Name: ss5-hdcpz				#软件包名，应与SPEC文件名一致
Version: 1.1 					#版本号
Release: 1%{?dist}  			#发行编码。初始值1%{?dist}
Summary: SS5 proxy install 		#软件包介绍
Group: Applications/Interne		#软件包组。 less /usr/share/doc/rpm-*/GROUPS" 可查组名
License: GPLv2+  				#授权协议，必须是开源许可证
Source0: %{name}-%{version}.tar.gz # SOURCES下的软件包
BuildRoot: %_topdir/BUILDROOT 	#默认值
BuildRequires: openldap-devel pam-devel openssl-devel  #安装依赖
%description 					#对程序进行描述
SS5 is a socks server		
%prep						#打包准备阶段执行的一些命令，源码包需要解压并切换目录，则
%setup -n ss5-3.8.9				需要下面这行命令 “%setup -n ss5-3.8.9”

%define __os_install_post /usr/lib/rpm/brp-compress; echo 'Not stripping.'

%global debug_package %{nil}			#构建RPM包，会自动打出debuginfo包，该命令可以不拆分debuginfo包

%build						#构建阶段执行的命令

./configure --with-libpath=%{_libdir} 	
make %{?_smp_mflags}

%install						#安装阶段执行的命令
rm -rf $RPM_BUILD_ROOT

make install prefix=$RPM_BUILD_ROOT 

chmod -R +r $RPM_BUILD_ROOT

%clean						#清理安装目录
rm -rf $RPM_BUILD_ROOT

%post						#添加ss5服务
chkconfig --add ss5

%preun						
if [ $1 = 0 ]; then
        /sbin/service ss5 stop > /dev/null 2>&1
        /sbin/chkconfig --del ss5
fi

%files						#需要打包的文件列表
%defattr(755,root,root)			#%defatter设置默认文件权限
%{_sbindir}/ss5				#%{_sbindir}安装文件，下面是ss5的一些文件
%{_sbindir}/ss5srv
%{_initrddir}/ss5
%{_libdir}/ss5/
%defattr(644,root,root)
%dir %{_docdir}/ss5
%{_docdir}/ss5/License
%{_docdir}/ss5/README.pam
%dir %{_docdir}/ss5/examples
%{_docdir}/ss5/examples/ss5.pam
%{_docdir}/ss5/README.ldap
%{_docdir}/ss5/examples/slapd.conf
%{_docdir}/ss5/examples/entries.ldif
%{_docdir}/ss5/README.statmgr
%{_mandir}/man1/ss5.1.gz
%{_mandir}/man1/ss5srv.1.gz
%{_mandir}/man5/ss5.passwd.5.gz
%{_mandir}/man5/ss5.ha.5.gz
%{_mandir}/man5/ss5.conf.5.gz
%{_mandir}/man5/ss5.pam.5.gz
%{_mandir}/man5/ss5_gss.5.gz
%{_mandir}/man5/ss5_supa.5.gz
%defattr(755,root,root)
%{_localstatedir}/log/ss5
%{_localstatedir}/run/ss5
%defattr(644,root,root)
%dir %{_sysconfdir}/opt/ss5
%config(noreplace) %{_sysconfdir}/opt/ss5/ss5.conf
%config(noreplace) %{_sysconfdir}/opt/ss5/ss5.passwd
%config(noreplace) %{_sysconfdir}/opt/ss5/ss5.ha
%config(noreplace) %{_sysconfdir}/pam.d/ss5
%config(noreplace) %{_sysconfdir}/sysconfig/ss5
%define __debug_install_post   \ %{_rpmconfigdir}/find-debuginfo.sh %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"\
%{nil}



2>存放SPEC文件
将.spec文件存放到~ ./rpmbuild/SPECS/ 文件下面

5、构建RPM
在~ ./rpmbuild/SPECS/ 文件夹下执行  
rpmbuild –ba NAME.spec
构建成功，RPM 会保存至 ~/rpmbuild/RPMS，SRPM 会保存至 ~/rpmbuild/SRPMS

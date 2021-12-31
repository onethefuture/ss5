Name: ss5-hdcpz 
Version: 1.1 
Release: 1%{?dist}  
Summary: SS5 proxy install 
Group: Applications/Interne
License: GPLv2+  
Source0: %{name}-%{version}.tar.gz 
BuildRoot: %_topdir/BUILDROOT 
BuildRequires: openldap-devel pam-devel openssl-devel 
#libgssapi-devel

%description 
SS5 is a socks server
%prep
%setup -n ss5-3.8.9

%define __os_install_post /usr/lib/rpm/brp-compress; echo 'Not stripping.'

%global debug_package %{nil}

%build

./configure --with-libpath=%{_libdir} 
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install prefix=$RPM_BUILD_ROOT 

chmod -R +r $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
chkconfig --add ss5

%preun
if [ $1 = 0 ]; then
        /sbin/service ss5 stop > /dev/null 2>&1
        /sbin/chkconfig --del ss5
fi

%files
%defattr(755,root,root)
%{_sbindir}/ss5
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
%{_docdir}/ss5/README.balamgr

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

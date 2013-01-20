Summary:	CacheFiles user-space management daemon
Name:		cachefilesd
Version:	0.10.5
Release:	0.1
License:	GPL v2
Group:		Daemons
URL:		http://people.redhat.com/~dhowells/fscache/
Source0:	http://people.redhat.com/dhowells/fscache/%{name}-%{version}.tar.bz2
# Source0-md5:	9e85dd0ace346ff47e188ded8c05ab3b
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units >= 38
Requires:	systemd-units >= 38
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The cachefilesd daemon manages the caching files and directory that
are that are used by network file systems such a AFS and NFS to do
persistent caching to the local disk.

%prep
%setup -q

%build
%{__make} CFLAGS="%{rpmcppflags} %{rpmcflags}" \
	all

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/sbin
install -d $RPM_BUILD_ROOT%{systemdunitdir}
install -d $RPM_BUILD_ROOT%{_mandir}/{man5,man8}
install -d $RPM_BUILD_ROOT%{_localstatedir}/cache/fscache

%{__make} DESTDIR=$RPM_BUILD_ROOT install

install cachefilesd.conf $RPM_BUILD_ROOT%{_sysconfdir}
install cachefilesd.service $RPM_BUILD_ROOT%{systemdunitdir}/cachefilesd.service

%clean
rm -rf $RPM_BUILD_ROOT

%post
#/sbin/chkconfig --add cachefilesd
%service cachefilesd restart "cachefilesd daemon"
%systemd_post cachefilesd.service

%preun
if [ "$1" = "0" ]; then
	%service cachefilesd stop
        #/sbin/chkconfig --del cachefilesd
fi
%systemd_preun cachefilesd.service

%postun
%systemd_reload

%files
%defattr(644,root,root,755)
%doc README howto.txt selinux/move-cache.txt
%doc selinux/*.fc selinux/*.if selinux/*.te
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cachefilesd.conf
/sbin/cachefilesd
%{systemdunitdir}/cachefilesd.service
%{_mandir}/man5/cachefilesd.conf.5*
%{_mandir}/man8/cachefilesd.8*
%dir %{_localstatedir}/cache/fscache

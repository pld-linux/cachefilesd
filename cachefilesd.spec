Summary:	CacheFiles user-space management daemon
Name:		cachefilesd
Version:	0.10.5
Release:	2
License:	GPL v2
Group:		Daemons
Source0:	http://people.redhat.com/dhowells/fscache/%{name}-%{version}.tar.bz2
# Source0-md5:	9e85dd0ace346ff47e188ded8c05ab3b
Source1:	%{name}.init
Patch0:		%{name}-cpueating.patch
URL:		http://people.redhat.com/~dhowells/fscache/
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units >= 38
Requires:	rc-scripts
Requires:	systemd-units >= 38
Requires:	uname(release) >= 2.6.30
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The cachefilesd daemon manages the caching files and directory that
are that are used by network file systems such a AFS and NFS to do
persistent caching to the local disk.

%prep
%setup -q
%patch0 -p1

%build
%{__make} all \
	CC="%{__cc}" \
	CFLAGS="%{rpmcppflags} %{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/sbin,%{_mandir}/man{5,8},%{systemdunitdir},/etc/rc.d/init.d,%{_localstatedir}/cache/fscache}

%{__make} install \
	INSTALL="install -p" \
	DESTDIR=$RPM_BUILD_ROOT

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/cachefilesd
cp -p cachefilesd.service $RPM_BUILD_ROOT%{systemdunitdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add cachefilesd
%service cachefilesd restart "cachefilesd daemon"
%systemd_post cachefilesd.service

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del cachefilesd
	%service cachefilesd stop
fi
%systemd_preun cachefilesd.service

%postun
%systemd_reload

%files
%defattr(644,root,root,755)
%doc README howto.txt selinux/move-cache.txt
%doc selinux/*.fc selinux/*.if selinux/*.te
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cachefilesd.conf
%attr(755,root,root) /sbin/cachefilesd
%{_mandir}/man5/cachefilesd.conf.5*
%{_mandir}/man8/cachefilesd.8*
%attr(754,root,root) /etc/rc.d/init.d/cachefilesd
%{systemdunitdir}/cachefilesd.service
%dir %{_localstatedir}/cache/fscache

Summary:	CacheFiles user-space management daemon
Summary(pl.UTF-8):	Demon przestrzeni użytkownika zarządzający pamięcią podręczną plików
Name:		cachefilesd
Version:	0.10.10
Release:	1
License:	GPL v2
Group:		Daemons
Source0:	https://people.redhat.com/dhowells/fscache/%{name}-%{version}.tar.bz2
# Source0-md5:	b440010d63ab18eebec63fe0328cba05
Source1:	%{name}.init
URL:		https://people.redhat.com/dhowells/fscache/
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

%description -l pl.UTF-8
Demon cachefilesd zarządza pamięcią podręczną plików i katalogów,
używaną przez sieciowe systemy plików, takie jak AFS i NFS do trwałego
buforowania na dysku lokalnym.

%prep
%setup -q

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
%doc README howto.txt selinux
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cachefilesd.conf
%attr(755,root,root) /sbin/cachefilesd
%{_mandir}/man5/cachefilesd.conf.5*
%{_mandir}/man8/cachefilesd.8*
%attr(754,root,root) /etc/rc.d/init.d/cachefilesd
%{systemdunitdir}/cachefilesd.service
%dir %{_localstatedir}/cache/fscache

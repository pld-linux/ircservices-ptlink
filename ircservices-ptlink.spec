Summary:	Internet Relay Chat Services
Summary(pl.UTF-8):	Usługi dla sieci IRC
Name:		ircservices-ptlink
Version:	2.25.1
Release:	1
License:	GPL v2
Group:		Daemons
Source0:	ftp://sunsite.dk/projects/ptlink/services2/PTlink.Services%{version}.tar.gz
# Source0-md5:	59df68440f40c7ef0e40090048fc7775
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-path.patch
URL:		http://www.ptlink.net/Coders/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	rpmbuild(macros) >= 1.202
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	rc-scripts
Provides:	group(ircd)
Provides:	user(ircd)
Obsoletes:	ircservices
Obsoletes:	ircservices6
Obsoletes:	ircservices-hybrid
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/ircservices
%define		_localstatedir	/var/lib/ircservices

%description
PTlink Services is a package of services for IRC networks.

%description -l pl.UTF-8
PTlink Services to pakiet z usługami dla sieci IRC (Internet Relay
Chat).

%prep
%setup -q -n PTlink.Services%{version}
%patch0 -p1

%build
cp -f %{_datadir}/automake/config.* autoconf
mv autoconf/configure.in .
%{__aclocal}
%{__autoconf}
CFLAGS="%{rpmcflags} %{?debug:-DDEBUGMODE}"
%configure
%{__make}
%{__make} -C src/lang

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/ircservices,%{_var}/log/ircservices,%{_sysconfdir}} \
	$RPM_BUILD_ROOT%{_sbindir} \
	$RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig},%{_localstatedir}/languages} \
	$RPM_BUILD_ROOT%{_var}/log/ircservices/

install src/services $RPM_BUILD_ROOT%{_sbindir}/ircservices
install data/example.conf	$RPM_BUILD_ROOT%{_sysconfdir}/services.conf
install data/domain.def	$RPM_BUILD_ROOT%{_sysconfdir}/domain.def
install data/nicks.plot	$RPM_BUILD_ROOT%{_sysconfdir}/nicks.plot
install data/ptlink.motd	$RPM_BUILD_ROOT%{_sysconfdir}/ptlink.motd
install src/lang/{en_us,pt,tr,de,it,nl,pt_br} $RPM_BUILD_ROOT%{_localstatedir}/languages

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ircservices
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/ircservices

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -f -g 75 ircd
%useradd -g ircd -d /etc/ircd -u 75 -c "IRC service account" -s /bin/true ircd

%post
/sbin/chkconfig --add ircd
if [ -f /var/lock/subsys/ircservices ]; then
	/etc/rc.d/init.d/ircservices restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/ircservices start\" to start IRC daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/ircservices ]; then
		/etc/rc.d/init.d/ircservices stop 1>&2
	fi
	/sbin/chkconfig --del ircservices
fi

%postun
if [ "$1" = "0" ]; then
	%userremove ircd
	%groupremove ircd
fi

%files
%defattr(644,root,root,755)
%doc FAQ FEATURES CHANGES README
%attr(755,root,root) %{_sbindir}/*
%attr(770,root,ircd) %dir %{_sysconfdir}
%attr(660,ircd,ircd) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%attr(754,root,root) /etc/rc.d/init.d/ircservices
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/ircservices
%dir %{_libdir}/ircservices
%dir %{_var}/log/ircservices
%attr(770,root,ircd) %dir %{_var}/log/ircservices
%attr(770,root,ircd) %dir %{_localstatedir}
%attr(770,root,ircd) %dir %{_localstatedir}/languages
%attr(660,root,ircd) %{_localstatedir}/languages/*

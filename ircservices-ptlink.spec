Summary:	Internet Relay Chat Services
Summary(pl):	Us³ugi dla sieci IRC
Name:		ircservices-ptlink
Version:	2.23.6
Release:	1
License:	GPL v2
Group:		Daemons
Source0:	ftp://sunsite.dk/projects/ptlink/PTlink.Services%{version}.tar.gz
# Source0-md5:	c952a18e181176c4af778bbe4893fa4b
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-path.patch
URL:		http://www.ptlink.net/Coders/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	zlib-devel
PreReq:		rc-scripts
Requires(pre):	/usr/bin/getgid
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/userdel
Requires(postun):	/usr/sbin/groupdel
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	ircservices
Obsoletes:	ircservices6
Obsoletes:	ircservices-hybrid

%define		_sysconfdir	/etc/ircservices
%define		_localstatedir	/var/lib/ircservices

%description
PTlink Services is a package of services for IRC networks.

%description -l pl
PTlink Services to pakiet z us³ugami dla sieci IRC (Internet Relay
Chat).

%prep
%setup -q -n PTlink.Services%{version}
%patch -p1

%build
mv -f autoconf/{configure.in,acconfig.h} .
cp -f %{_datadir}/automake/config.* autoconf
%{__aclocal}
%{__autoconf}
CFLAGS="%{rpmcflags} %{?debug:-DDEBUGMODE}"
%configure
echo '!SUB!THIS!' >> src/version.c.SH
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
if [ -n "`getgid ircd`" ]; then
	if [ "`getgid ircd`" != "75" ]; then
		echo "Error: group ircd doesn't have gid=75. Correct this before installing ircd." 1>&2
		exit 1
	fi
else
	/usr/sbin/groupadd -f -g 75 ircd 2> /dev/null
fi
if [ -n "`id -u ircd 2>/dev/null`" ]; then
	if [ "`id -u ircd`" != "75" ]; then
		echo "Error: user ircd doesn't have uid=75. Correct this before installing ircd." 1>&2
		exit 1
	fi
else
	/usr/sbin/useradd -g ircd -d /etc/ircd -u 75 -c "IRC service account" -s /bin/true ircd 2> /dev/null
fi

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

#%postun
#if [ "$1" = "0" ]; then
#	/usr/sbin/userdel ircservices 2> /dev/null
#	/usr/sbin/groupdel ircservices 2> /dev/null
#fi

%files
%defattr(644,root,root,755)
%doc FAQ FEATURES CHANGES README
%attr(755,root,root) %{_sbindir}/*
%attr(770,root,ircd) %dir %{_sysconfdir}
%attr(660,ircd,ircd) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*
%attr(754,root,root) /etc/rc.d/init.d/ircservices
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/ircservices
%dir %{_libdir}/ircservices
%dir %{_var}/log/ircservices
%attr(770,root,ircd) %dir %{_var}/log/ircservices
%attr(770,root,ircd) %dir %{_localstatedir}
%attr(770,root,ircd) %dir %{_localstatedir}/languages
%attr(660,root,ircd) %{_localstatedir}/languages/*

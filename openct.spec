Summary:	OpenCT library - library for accessing smart card terminals
Summary(pl.UTF-8):	OpenCT - biblioteka dostępu do terminali kart procesorowych
Name:		openct
Version:	0.6.15
Release:	3
License:	LGPL v2.1+
Group:		Applications/System
Source0:	http://www.opensc-project.org/files/openct/%{name}-%{version}.tar.gz
# Source0-md5:	70205beac03974e266fc259b6c9feaa8
Source1:	%{name}.init
URL:		http://www.opensc-project.org/openct/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	libltdl-devel
BuildRequires:	libtool
BuildRequires:	libusb-devel
BuildRequires:	pcsc-lite-devel
BuildRequires:	pkgconfig >= 1:0.9.0
Requires(post,preun):	/sbin/chkconfig
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/userdel
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenCT is a library for accessing smart card terminals. It provides a
rich set of functions for driver writers, protocol drivers for T=0 and
T=1, serial and USB functionality, including USB hotplugging. 

%description -l pl.UTF-8
OpenCT to biblioteka służąca do dostępu do terminali kart
procesorowych (smart card). Dostarcza bogaty zbiór funkcji dla
piszących sterowniki, sterowniki protokołów dla T=0 i T=1,
funkcjonalność dla portów szeregowych i USB, włącznie z podłączaniem
urządzeń USB w locie (hotplug).

%package -n hal-openct
Summary:	hal integration for OpenCT
Summary(pl.UTF-8):	Integracja OpenCT z hal
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	udev-core

%description -n hal-openct
hal integration for OpenCT.

%description -n hal-openct -l pl.UTF-8
Integracja OpenCT z hal.

%package -n udev-openct
Summary:	udev integration for OpenCT
Summary(pl.UTF-8):	Integracja OpenCT z udevem
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	udev-core

%description -n udev-openct
udev integration for OpenCT.

%description -n udev-openct -l pl.UTF-8
Integracja OpenCT z udevem.

%package -n pcsc-driver-openct
Summary:	OpenCT driver for PC/SC
Summary(pl.UTF-8):	Sterownik OpenCT dla PC/SC
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pcsc-lite

%description -n pcsc-driver-openct
OpenCT driver for PC/SC.

%description -n pcsc-driver-openct -l pl.UTF-8
Sterownik OpenCT dla PC/SC.

%package libs
Summary:	OpenCT library
Summary(pl.UTF-8):	Biblioteka OpenCT
License:	BSD (libopenct), LGPL v2.1+ (the rest)
Group:		Libraries
Conflicts:	openct < 0.6.2-3

%description libs
OpenCT library.

%description libs -l pl.UTF-8
Biblioteka OpenCT.

%package devel
Summary:	OpenCT development files
Summary(pl.UTF-8):	Pliki dla programistów używających OpenCT
License:	BSD
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
OpenSC development files.

%description devel -l pl.UTF-8
Pliki dla programistów używających OpenCT.

%package static
Summary:	Static OpenCT libraries
Summary(pl.UTF-8):	Bibloteki statyczne OpenCT
License:	BSD
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static OpenCT libraries.

%description static -l pl.UTF-8
Statyczne biblioteki OpenCT.

%prep
%setup -q

%build
touch config.rpath
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-rpath \
	--enable-api-doc \
	--enable-non-privileged \
	--enable-pcsc \
	--enable-sunray \
	--enable-sunrayclient \
	--enable-usb \
	--with-apidocdir \
	--with-bundle=%{_libdir}/pcsc/drivers \
	--with-ifddir \
	--with-udev=/lib/udev
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/var/run/openct,/etc/{rc.d/init.d,udev/rules.d},/usr/share/hal/fdi/information/10freedesktop}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install etc/openct.conf $RPM_BUILD_ROOT%{_sysconfdir}
install etc/openct.fdi $RPM_BUILD_ROOT%{_datadir}/hal/fdi/information/10freedesktop/10-usb-openct.fdi
install etc/openct.hald $RPM_BUILD_ROOT%{_bindir}/hald-addon-openct
install etc/openct.udev $RPM_BUILD_ROOT/etc/udev/rules.d/50-openct.rules

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/openct

rm -f $RPM_BUILD_ROOT%{_libdir}/openct-*.{a,la}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%useradd -u 208 -d %{_datadir}/empty -c "openctd User" -g usb openctd

%post
/sbin/chkconfig --add openct
if [ -f /var/lock/subsys/openct ]; then
	/etc/rc.d/init.d/openct restart >&2
else
	echo "Run \"/etc/rc.d/init.d/openct start\" to start openct."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/openct ]; then
		/etc/rc.d/init.d/openct stop >&2
	fi
	/sbin/chkconfig --del openct
fi

%postun
if [ "$1" = "0" ]; then
	%userremove openctd
fi

%post   libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS TODO doc/nonpersistent/ChangeLog doc/nonpersistent/wiki.out/*.{html,css}
%attr(755,root,root) %{_bindir}/openct-tool
%attr(755,root,root) %{_sbindir}/ifdhandler
%attr(755,root,root) %{_sbindir}/ifdproxy
%attr(755,root,root) %{_sbindir}/openct-control
%dir /var/run/openct
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/openct.conf
%attr(754,root,root) /etc/rc.d/init.d/openct
%{_mandir}/man1/openct-tool.1*

%files -n udev-openct
%defattr(644,root,root,755)
%attr(755,root,root) /lib/udev/openct_pcmcia
%attr(755,root,root) /lib/udev/openct_serial
%attr(755,root,root) /lib/udev/openct_usb
%config(noreplace) %verify(not md5 mtime size) /etc/udev/rules.d/50-openct.rules

%files -n hal-openct
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/hald-addon-openct
%{_datadir}/hal/fdi/information/10freedesktop/10-usb-openct.fdi

%files -n pcsc-driver-openct
%defattr(644,root,root,755)
%dir %{_libdir}/pcsc/drivers/openct-ifd.bundle
%dir %{_libdir}/pcsc/drivers/openct-ifd.bundle/Contents
%dir %{_libdir}/pcsc/drivers/openct-ifd.bundle/Contents/Linux
%attr(755,root,root) %dir %{_libdir}/pcsc/drivers/openct-ifd.bundle/Contents/Linux/openct-ifd.so
%{_libdir}/pcsc/drivers/openct-ifd.bundle/Contents/Info.plist
%{_libdir}/pcsc/drivers/openct-ifd.bundle/Contents/PkgInfo

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libopenct.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopenct.so.1
%attr(755,root,root) %{_libdir}/libopenctapi.so
%attr(755,root,root) %{_libdir}/openct-ifd.so

%files devel
%defattr(644,root,root,755)
%doc doc/api.out/html/*
%attr(755,root,root) %{_libdir}/libopenct.so
%{_libdir}/libopenct.la
%{_libdir}/libopenctapi.la
%{_includedir}/openct
%{_pkgconfigdir}/libopenct.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libopenct.a
%{_libdir}/libopenctapi.a

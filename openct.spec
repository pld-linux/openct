Summary:	OpenCT library - library for accessing smart card terminals
Summary(pl.UTF-8):	OpenCT - biblioteka dostępu do terminali kart procesorowych
Name:		openct
Version:	0.6.20
Release:	4
License:	LGPL v2.1+
Group:		Applications/System
#Source0Download: https://github.com/OpenSC/openct/releases
Source0:	http://downloads.sourceforge.net/opensc/%{name}-%{version}.tar.gz
# Source0-md5:	a1da3358ab798f1cb9232f1dbababc21
Source1:	%{name}.init
Source2:	%{name}.tmpfiles
URL:		https://github.com/OpenSC/openct/wiki
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	libltdl-devel
BuildRequires:	libtool
BuildRequires:	libusb-compat-devel
BuildRequires:	pcsc-lite-devel
BuildRequires:	pkgconfig >= 1:0.9.0
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
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

%package -n udev-openct
Summary:	udev integration for OpenCT
Summary(pl.UTF-8):	Integracja OpenCT z udevem
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	udev-core
Obsoletes:	hal-openct

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
Group:		Libraries
Conflicts:	openct < 0.6.2-3

%description libs
OpenCT library.

%description libs -l pl.UTF-8
Biblioteka OpenCT.

%package devel
Summary:	OpenCT development files
Summary(pl.UTF-8):	Pliki dla programistów używających OpenCT
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
OpenSC development files.

%description devel -l pl.UTF-8
Pliki dla programistów używających OpenCT.

%package static
Summary:	Static OpenCT libraries
Summary(pl.UTF-8):	Bibloteki statyczne OpenCT
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
install -d $RPM_BUILD_ROOT{/var/run/openct,/etc/{rc.d/init.d,udev/rules.d}} \
	$RPM_BUILD_ROOT/usr/lib/tmpfiles.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -a etc/openct.conf $RPM_BUILD_ROOT%{_sysconfdir}
cp -a etc/openct.udev $RPM_BUILD_ROOT/etc/udev/rules.d/50-openct.rules
install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/openct
install -p %{SOURCE2} $RPM_BUILD_ROOT/usr/lib/tmpfiles.d/%{name}.conf

rm -f $RPM_BUILD_ROOT%{_libdir}/openct-*.{a,la}
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%useradd -u 208 -d %{_datadir}/empty -c "openctd User" -g usb openctd

%post
/sbin/chkconfig --add openct
%service openct restart

%preun
if [ "$1" = "0" ]; then
	%service openct stop
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
/usr/lib/tmpfiles.d/%{name}.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/openct.conf
%attr(754,root,root) /etc/rc.d/init.d/openct
%{_mandir}/man1/openct-tool.1*

%files -n udev-openct
%defattr(644,root,root,755)
%attr(755,root,root) /lib/udev/openct_pcmcia
%attr(755,root,root) /lib/udev/openct_serial
%attr(755,root,root) /lib/udev/openct_usb
%config(noreplace) %verify(not md5 mtime size) /etc/udev/rules.d/50-openct.rules

%files -n pcsc-driver-openct
%defattr(644,root,root,755)
%dir %{_libdir}/pcsc/drivers/openct-ifd.bundle
%dir %{_libdir}/pcsc/drivers/openct-ifd.bundle/Contents
%dir %{_libdir}/pcsc/drivers/openct-ifd.bundle/Contents/Linux
%attr(755,root,root) %{_libdir}/pcsc/drivers/openct-ifd.bundle/Contents/Linux/openct-ifd.so
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

# TODO: move hotplug and udev stuff to subpackages?
Summary:	OpenCT library - library for accessing smart card terminals
Summary(pl):	OpenCT - biblioteka dostêpu do terminali kart procesorowych
Name:		openct
Version:	0.6.10
Release:	1
License:	LGPL
Group:		Applications
Source0:	http://www.opensc-project.org/files/openct/%{name}-%{version}.tar.gz
# Source0-md5:	fc91a7cda636b0dc5de74f1d22c2d914
Source1:	%{name}.init
URL:		http://www.opensc-project.org/openct/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	libusb-devel
BuildRequires:	pcsc-lite-devel
BuildRequires:	pkgconfig >= 1:0.9.0
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenCT is a library for accessing smart card terminals. It provides a
rich set of functions for driver writers, protocol drivers for T=0 and
T=1, serial and USB functionality, including USB hotplugging. 

%description -l pl
OpenCT to biblioteka s³u¿±ca do dostêpu do terminali kart
procesorowych (smart card). Dostarcza bogaty zbiór funkcji dla
pisz±cych sterowniki, sterowniki protoko³ów dla T=0 i T=1,
funkcjonalno¶æ dla portów szeregowych i USB, w³±cznie z pod³±czaniem
urz±dzeñ USB w locie (hotplug).

%package -n pcsc-driver-openct
Summary:	OpenCT driver for PC/SC
Summary(pl):	Sterownik OpenCT dla PC/SC
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pcsc-lite

%description -n pcsc-driver-openct
OpenCT driver for PC/SC.

%description -n pcsc-driver-openct -l pl
Sterownik OpenCT dla PC/SC.

%package libs
Summary:	OpenCT library
Summary(pl):	Biblioteka OpenCT
License:	BSD (libopenct), LGPL (the rest)
Group:		Libraries
Conflicts:	openct < 0.6.2-3

%description libs
OpenCT library.

%description libs -l pl
Biblioteka OpenCT.

%package devel
Summary:	OpenCT development files
Summary(pl):	Pliki dla programistów u¿ywaj±cych OpenCT
License:	BSD
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
OpenSC development files.

%description devel -l pl
Pliki dla programistów u¿ywaj±cych OpenCT.

%package static
Summary:	Static OpenCT libraries
Summary(pl):	Bibloteki statyczne OpenCT
License:	BSD
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static OpenCT libraries.

%description static -l pl
Statyczne biblioteki OpenCT.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I aclocal
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-bundle-dir=%{_libdir}/pcsc/drivers
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/hotplug/usb,/lib/udev,/var/run/openct}
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install etc/openct.conf $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/openct

rm -f $RPM_BUILD_ROOT%{_libdir}/openct-*.{a,la}

%clean
rm -rf $RPM_BUILD_ROOT

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

%post   libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS TODO doc/ChangeLog doc/*.{html,css}
%attr(755,root,root) %{_bindir}/openct-tool
%attr(755,root,root) %{_sbindir}/ifdhandler
%attr(755,root,root) %{_sbindir}/ifdproxy
%attr(755,root,root) %{_sbindir}/openct-control
%dir /var/run/openct
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/openct.conf
%{_sysconfdir}/hotplug/usb/openct.usermap
%attr(755,root,root) /lib/udev/openct_*
%attr(754,root,root) /etc/rc.d/init.d/openct
%{_mandir}/man1/openct-tool.1*

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
%attr(755,root,root) %{_libdir}/libopenctapi.so
%attr(755,root,root) %{_libdir}/openct-ifd.so

%files devel
%defattr(644,root,root,755)
%doc doc/api/*
%attr(755,root,root) %{_libdir}/libopenct.so
%{_libdir}/libopenct.la
%{_libdir}/libopenctapi.la
%{_includedir}/openct
%{_pkgconfigdir}/libopenct.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libopenct.a
%{_libdir}/libopenctapi.a

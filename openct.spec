# TODO:
# - write init script
Summary:	OpenCT library - library for accessing smart card terminals
Summary(pl):	OpenCT - biblioteka dostêpu do terminali kart procesorowych
Name:		openct
Version:	0.5.0
Release:	0.2
License:	BSD-like
Group:		Applications
Source0:	http://www.opensc.org/files/%{name}-%{version}.tar.gz
# Source0-md5:	5e6de721d22db8f5da060a1843bb3259
URL:		http://www.opensc.org/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	libusb-devel
BuildRequires:	pcsc-lite-devel
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

%package devel
Summary:	OpenCT development files
Summary(pl):	Pliki dla programistów u¿ywaj±cych OpenCT
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
OpenSC development files.

%description devel -l pl
Pliki dla programistów u¿ywaj±cych OpenCT.

%package static
Summary:	Static OpenCT libraries
Summary(pl):	Bibloteki statyczne OpenCT
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static OpenCT libraries.

%description static -l pl
Statyczne biblioteki OpenCT.

%prep
%setup -q

%build
%configure 
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/hotplug/usb

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install etc/openct.conf $RPM_BUILD_ROOT%{_sysconfdir}

rm -f $RPM_BUILD_ROOT%{_libdir}/openct-*.{a,la}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ANNOUNCE ChangeLog NEWS TODO doc/openct.{html,css}
%attr(755,root,root) %{_bindir}/openct-tool
%attr(755,root,root) %{_sbindir}/ifdhandler
%attr(755,root,root) %{_sbindir}/openct-control
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%attr(755,root,root) %{_libdir}/openct-*.so
%attr(755,root,root) %{_libdir}/libopenctapi.so
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/openct.conf
%attr(755,root,root) %{_sysconfdir}/hotplug/usb/openct
%{_sysconfdir}/hotplug/usb/openct.usermap

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libifd.so
%attr(755,root,root) %{_libdir}/libopenct.so
%{_libdir}/lib*.la
%{_includedir}/openct
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

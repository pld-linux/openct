# TODO:
# - install openct.conf
# - write init script
Summary:	OpenCT library - library for accessing smart card terminals
Name:		openct
Version:	0.1.0
Release:	0.1
License:	BSD-like ?
Group:		Applications
Source0:	http://www.opensc.org/files/%{name}-%{version}.tar.gz
# Source0-md5:	d405dea25b657475053539e6ffb66135
URL:		http://www.opensc.org/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	libusb-devel
BuildRequires:	pcsc-lite-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenCT is a library for accessing smart card terminals.  It provides a rich set
of functions for driver writers, protocol drivers for T=0 and T=1, serial and
USB functionality, including USB hotplugging. 

%package devel
Summary:	OpenCT development files
Summary(pl):	Pliki dla programistów u¿ywaj±cych OpenCT
Group:		Development/Tools
Requires:	%{name} = %{version}

%description devel
OpenSC development files.

%description devel -l pl
Pliki dla programistów u¿ywaj±cych OpenCT.

%package static
Summary:	Static OpenCT libraries
Summary(pl):	Bibloteki statyczne OpenCT
Group:		Development/Tools
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

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/openct-*.{a|la}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ANNOUNCE ChangeLog NEWS doc/openct.{html,css}
%attr(755,root,root) %{_bindir}/openct-tool
%attr(755,root,root) %{_sbindir}/hotplug.openct
%attr(755,root,root) %{_sbindir}/ifdhandler
%attr(755,root,root) %{_sbindir}/openct-control
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%attr(755,root,root) %{_libdir}/openct-*.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/openct
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

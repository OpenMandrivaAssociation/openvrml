%define lib_major 0
%define libname %mklibname %{name} %{lib_major}
%define develname %mklibname -d %{name}

Name:       openvrml
Version:    0.17.5
Release:    %mkrel 1
Summary:    A free cross-platform runtime for VRML and X3D
License:    LGPL
Group:      Graphics
URL:        http://openvrml.org/
Source0:    http://downloads.sourceforge.net/openvrml/%{name}-%{version}.tar.gz
BuildRequires:  SDL-devel
BuildRequires:  mesagl-devel
BuildRequires:  gtk+2-devel
BuildRequires:  libxmu-devel
BuildRequires:  doxygen
BuildRequires:  boost-devel
BuildRequires:  js-devel
BuildRequires:  curl-devel
BuildRequires:  mozilla-firefox-devel
BuildRequires:  libglade2-devel
BuildRequires:  libgnomeui2-devel
BuildRoot:  %{_tmppath}/%{name}-%{version}

%description
OpenVRML is a free cross-platform runtime for VRML and X3D available under the
GNU Lesser General Public License. The OpenVRML distribution includes libraries
you can use to add VRML/X3D support to an application. On platforms where GTK+
is available, OpenVRML also provides a plug-in to render VRML/X3D worlds in Web
browsers.

%package -n %{libname}
Summary:	Dynamic libraries for %{name}
Group:		System/Libraries
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{libname}
This packages contains dynamic libraries for %{name}.

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}

%description -n %{develname}
This packages contains development files for %{name}.

%package plugins
Summary:	Mozilla %{name} plugins
Group:      Graphics

%description plugins
This package contain the %{name} plugins for mozilla.

%package doc
Summary:	Documentation for %{name}
Group:      Graphics

%description doc
This package contain the documentation for %{name}.

%prep
%setup -q

%build
%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std docdir=%{_docdir}/%{name}

%clean
rm -rf %{buildroot}

%post
%_install_info openvrml-xembed

%post -n %{libname} -p /sbin/ldconfig

%preun
%_remove_install_info openvrml

%postun -n %{libname} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS COPYING COPYING.LESSER INSTALL NEWS README THANKS
%{_bindir}/openvrml-player
%{_libdir}/openvrml-xembed
%{_datadir}/openvrml-player
%{_infodir}/openvrml-xembed.info*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_includedir}/openvrml
%{_libdir}/pkgconfig/*

%files plugins
%defattr(-,root,root)
%doc %{_docdir}/%{name}/manual
%{_libdir}/mozilla/plugins/*

%files doc
%defattr(-,root,root)
%doc %{_docdir}/%{name}/manual

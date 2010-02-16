%define lib_major 9
%define libname %mklibname %{name} %{lib_major}
%define libgl_major 8
%define libgl %mklibname %{name}-gl %{libgl_major}
%define develname %mklibname -d %{name}

%define _requires_exceptions devel(lib\\(mozjs\\|nspr4\\|plc4\\|plds4\\)\\((64bit)\\)\\?) 

Name:       openvrml
Version:    0.18.5
Release:    %mkrel 1
Summary:    A free cross-platform runtime for VRML and X3D
License:    LGPL
Group:      Graphics
URL:        http://openvrml.org/
Source0:    http://downloads.sourceforge.net/openvrml/%{name}-%{version}.tar.gz
Patch0:		openvrml-0.18.3-fix-str-fmt.patch
Patch1:		openvrml-0.18.3-fix-linkage.patch
Patch2:		openvrml-0.18.5-fix-format-errors.patch
BuildRequires:  SDL-devel
BuildRequires:  mesagl-devel
BuildRequires:  gtk+2-devel
BuildRequires:  libxmu-devel
BuildRequires:  doxygen
BuildRequires:  boost-devel
BuildRequires:  js-devel
BuildRequires:  curl-devel
BuildRequires:  xulrunner-devel
BuildRequires:  libglade2-devel
BuildRequires:  libgnomeui2-devel
BuildRequires:	libtool-devel
BuildRequires:	gtkglext-devel
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

%description -n %{libname}
This packages contains dynamic libraries for %{name}.

%package -n %{libgl}
Summary:        Dynamic libraries for %{name}
Group:          System/Libraries

%description -n %{libgl}
This packages contains dynamic libraries for %{name}.

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libgl} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
This packages contains development files for %{name}.

%package plugins
Summary:	Mozilla %{name} plugins
Group:      Graphics
Requires:   %{name} = %{version}-%{release}

%description plugins
This package contain the %{name} plugins for mozilla.

%package doc
Summary:	Documentation for %{name}
Group:      Graphics

%description doc
This package contain the documentation for %{name}.

%prep
%setup -q
%patch0 -p0
%patch1 -p0
%patch2 -p1

%build
%configure2_5x --disable-script-node-java --disable-static
%make

%install
rm -rf %{buildroot}
%makeinstall_std docdir=%{_docdir}/%{name}
# install manually, as %doc macro remove already existing directory
install -m  644 AUTHORS ChangeLog COPYING COPYING.LESSER INSTALL NEWS \
    README THANKS %{buildroot}%{_docdir}/%{name}

find %{buildroot} -name *.la | xargs rm

%clean
rm -rf %{buildroot}

%post
%_install_info openvrml-xembed

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%preun
%_remove_install_info openvrml

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root)
%{_docdir}/%{name}
%exclude %{_docdir}/%{name}/manual
%{_bindir}/openvrml-player
%{_libdir}/openvrml
%{_libdir}/openvrml-xembed
%{_datadir}/openvrml
%{_datadir}/openvrml-player
%{_datadir}/openvrml-xembed
%{_datadir}/dbus-1/services/org.openvrml.BrowserControl.service

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libopenvrml.so.%{lib_major}*

%files -n %{libgl}
%defattr(-,root,root)
%{_libdir}/libopenvrml-gl.so.%{libgl_major}*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/*.so
%{_includedir}/openvrml
%{_libdir}/pkgconfig/*

%files plugins
%defattr(-,root,root)
%{_libdir}/mozilla/plugins/*

%files doc
%defattr(-,root,root)
%{_docdir}/%{name}/manual
%{_datadir}/javadoc/%{name}-%{version}

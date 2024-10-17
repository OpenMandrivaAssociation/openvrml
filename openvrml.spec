%define major	9
%define glmajor	8
%define libname	%mklibname %{name} %{major}
%define libgl	%mklibname %{name}-gl %{glmajor}
%define devname	%mklibname -d %{name}

%if %{_use_internal_dependency_generator}
%define __noautoreq 'devel\\(lib(mozjs|nspr4|plc4|plds4)(\\(64bit\\))?\\)' 
%else
%define _requires_exceptions devel(lib\\(mozjs\\|nspr4\\|plc4\\|plds4\\)\\((64bit)\\)\\?) 
%endif

Summary:	A free cross-platform runtime for VRML and X3D
Name:		openvrml
Version:	0.18.9
Release:	2
License:	GPLv3 and LGPLv3
Group:		Graphics
URL:		https://openvrml.org/
Source0:	http://downloads.sourceforge.net/openvrml/%{name}-%{version}.tar.gz
Patch0:		openvrml-0.18.3-fix-str-fmt.patch
Patch2:		openvrml-0.18.5-fix-format-errors.patch
Patch3:		openvrml-0.18.9-format_security.patch

BuildRequires:	doxygen
BuildRequires:	boost-devel
BuildRequires:	libtool-devel
BuildRequires:	xulrunner-devel
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(gtkglext-1.0)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libglade-2.0)
BuildRequires:	pkgconfig(libgnomeui-2.0)
BuildRequires:	pkgconfig(libjs)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(xmu)

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
Summary:	Dynamic libraries for %{name}
Group:		System/Libraries

%description -n %{libgl}
This packages contains dynamic libraries for %{name}.

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libgl} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This packages contains development files for %{name}.

%package plugins
Summary:	Mozilla %{name} plugins
Group:		Graphics
Requires:	%{name} = %{version}-%{release}

%description plugins
This package contain the %{name} plugins for mozilla.

%package doc
Summary:	Documentation for %{name}
Group:		Graphics

%description doc
This package contain the documentation for %{name}.

%prep
%setup -q
#patch0 -p0
%patch2 -p1
%patch3 -p1

%build
%configure2_5x \
	--disable-static \
	--disable-script-node-java

%make

%install
%makeinstall_std docdir=%{_docdir}/%{name}
# install manually, as %doc macro remove already existing directory
install -m  644 AUTHORS ChangeLog COPYING COPYING.LESSER INSTALL NEWS \
    README THANKS %{buildroot}%{_docdir}/%{name}

find %{buildroot} -name *.la | xargs rm

%if %{mdvver} < 201200
%post
%_install_info openvrml-xembed

%preun
%_remove_install_info openvrml
%endif

%files
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
%{_libdir}/libopenvrml.so.%{major}*

%files -n %{libgl}
%{_libdir}/libopenvrml-gl.so.%{glmajor}*

%files -n %{devname}
%{_libdir}/*.so
%{_includedir}/openvrml
%{_libdir}/pkgconfig/*

%files plugins
%{_libdir}/mozilla/plugins/*

%files doc
%{_docdir}/%{name}/manual
%{_datadir}/javadoc/%{name}-%{version}


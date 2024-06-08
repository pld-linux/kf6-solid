#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	6.3
%define		qtver		5.15.2
%define		kfname		solid

Summary:	Desktop hardware abstraction
Name:		kf6-%{kfname}
Version:	6.3.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	f55c5d4a7c8ba1d1d6e70283f1297e32
URL:		http://www.kde.org/
BuildRequires:	Qt6Concurrent-devel >= %{qtver}
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6DBus-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Qml-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	Qt6Xml-devel >= %{qtver}
BuildRequires:	bison >= 3.0
BuildRequires:	cmake >= 3.16
BuildRequires:	flex
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	libimobiledevice-devel
BuildRequires:	libmount-devel
BuildRequires:	libplist-devel
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	qt6-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel
BuildRequires:	xz
Requires:	Qt6Core >= %{qtver}
Requires:	Qt6DBus >= %{qtver}
Requires:	Qt6Gui >= %{qtver}
Requires:	Qt6Qml >= %{qtver}
Requires:	Qt6Xml >= %{qtver}
Requires:	kf6-dirs
#Obsoletes:	kf5-%{kfname} < %{version}
Suggests:	media-player-info
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
Solid is a device integration framework. It provides a way of querying
and interacting with hardware independently of the underlying
operating system.

It provides the following features for application developers:

- Hardware Discovery
- Power Management
- Network Management


%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt6Core-devel >= %{qtver}
Requires:	cmake >= 3.16
#Obsoletes:	kf5-%{kfname}-devel < %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname}6_qt --with-qm --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kfname}6_qt.lang
%defattr(644,root,root,755)
%doc README.md TODO
%attr(755,root,root) %{_bindir}/solid-hardware6
%ghost %{_libdir}/libKF6Solid.so.6
%attr(755,root,root) %{_libdir}/libKF6Solid.so.*.*
%{_datadir}/qlogging-categories6/solid.categories
%{_datadir}/qlogging-categories6/solid.renamecategories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/Solid
%{_libdir}/cmake/KF6Solid
%{_libdir}/libKF6Solid.so

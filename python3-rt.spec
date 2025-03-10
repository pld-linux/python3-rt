# Conditional build:
%bcond_without	doc	# API documentation
# Tests need real rt server
%bcond_with	tests	# unit tests

%define		module	rt
Summary:	Python interface to Request Tracker API
Summary(pl.UTF-8):	-
Name:		python3-%{module}
Version:	3.0.0
Release:	2
License:	GPL v3
Group:		Libraries/Python
Source0:	https://pypi.debian.net/rt/%{module}-%{version}.tar.gz
# Source0-md5:	d435c28902ed9e50b567adee4b1d8e27
URL:		https://github.com/CZ-NIC/python-rt
BuildRequires:	python3-modules >= 1:3.2
%if %{with tests}
BuildRequires:	python3-nose
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-furo
BuildRequires:	python3-sphinx_copybutton
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python implementation of REST API described here:
https://rt-wiki.bestpractical.com/wiki/REST.

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation

%description apidocs
API documentation for Python %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd) \
%{__python3} test_rt.py
%endif

%if %{with doc}
%{__make} -C doc html \
	SPHINXBUILD=sphinx-build-3
rm -rf docs/_build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG.md README.rst
%dir %{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}/*.py
# PEP-561
%{py3_sitescriptdir}/%{module}/py.typed
%{py3_sitescriptdir}/%{module}/__pycache__
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html/*
%endif

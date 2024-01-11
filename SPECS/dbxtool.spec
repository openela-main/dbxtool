Name:           dbxtool
Version:        8
Release:        5%{?dist}.2
Summary:        Secure Boot DBX updater
License:        GPLv2
URL:            https://github.com/vathpela/dbxtool
ExclusiveArch:  i386 x86_64 aarch64
BuildRequires:  popt-devel git systemd
BuildRequires:  efivar-devel >= 31-3
Requires:       efivar >= 31-3
Requires(post): systemd
Requires(preun):systemd
Source0:        https://github.com/vathpela/dbxtool/releases/download/dbxtool-%{version}/dbxtool-%{version}.tar.bz2
Patch0000:      %{name}-8-ccldflags.patch
Patch0001:      0001-don-t-use-f-in-dbxtool.service.patch
Patch0002:      0002-Make-quiet-exit-on-missing-PK-KEK-not-return-error-s.patch
Patch0003:      0003-fix-relop-in-esl_iter_next.patch

%description
This package contains DBX updates for UEFI Secure Boot.

%prep
%setup -q -n %{name}-%{version}
git init
git config user.email "%{name}-owner@fedoraproject.org"
git config user.name "Fedora Ninjas"
git add .
git commit -a -q -m "%{version} baseline."
git am %{patches} </dev/null
git config --unset user.email
git config --unset user.name

%build
make PREFIX=%{_prefix} LIBDIR=%{_libdir} CFLAGS="$RPM_OPT_FLAGS" CCLDFLAGS="%{__global_ldflags}"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}/%{_libdir}
make PREFIX=%{_prefix} LIBDIR=%{_libdir} INSTALLROOT=%{buildroot} \
        install
rm -f %{buildroot}/%{_docdir}/%{name}/COPYING

%post
%systemd_post dbxtool.service

%preun
%systemd_preun dbxtool.service

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_bindir}/dbxtool
%doc %{_mandir}/man1/*
%dir %{_datadir}/dbxtool/
%{_datadir}/dbxtool/*.bin
%{_unitdir}/dbxtool.service

%changelog
* Wed Jan 20 2021 Jan Hlavac <jhlavac@redhat.com> - 8-5.el8_3.2
- Enable manual gating
  Related: rhbz#1681753
  Related: rhbz#1912474

* Fri Jan 15 2021 Javier Martinez Canillas <javierm@redhat.com> - 8-5.el8_3.1
- Fix 'EFI Signature List is malformed' error (lersek)
  Resolves: rhbz#1912474

* Thu Apr 12 2018 Petr Šabata <contyk@redhat.com> - 8-5
- Fix build flags injection (rhbz#1548123)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Oct 23 2017 Peter Jones <pjones@redhat.com> - 8-3
- Also don't return error if we're using --quiet and PK/KEK are absent.
  Resolves: rhbz#1489942

* Thu Oct 19 2017 Peter Jones <pjones@redhat.com> - 8-2
- Don't use -f in dbxtool.service; that'll make it do the thing we're
  trying to avoid.
  Resolves: rhbz#1489942

* Wed Oct 18 2017 Peter Jones <pjones@redhat.com> - 8-1
- Update to dbxtool 8
- Make a "make coverity" rule to scan the source
  Results at: https://scan.coverity.com/projects/rhboot-dbxtool
- Don't try to apply anything if PK and KEK aren't enrolled
- Add --force and --quiet for the PK/KEK checker, and use them in the
  systemd service.
  Resolves: rhbz#1489942
- Add a .syntastic_c_config for vim's Syntastic modules
- Use tsearch()/tfind()/tdestroy() from libc instead of ccan htables
- Don't open the dbx file with O_RDWR|O_CREAT, use O_RDONLY.
- Lots of minor bug fixes gcc -Wextra and friends found.

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jul 08 2017 Peter Jones <pjones@redhat.com> - 7-4
- Rebuild for efivar-31-1.fc26
  Related: rhbz#1468841

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Aug 17 2016 Peter Jones <pjones@redhat.com> - 7-2
- Rebuild for newer efivar.

* Wed Aug 10 2016 Peter Jones <pjones@redhat.com> - 7-1
- Update to version 7
- Add new dbxupdate.bin for CVE-2016-3320 and
  https://support.microsoft.com/en-us/kb/3179577

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Feb 23 2015 Peter Jones <pjones@redhat.com> - 0.6-4
- Zbigniew Jędrzejewski-Szmek was kind enough to audit the systemd service,
  and had some suggestions, as did Harald Hoyer and Lennart Poettering.
  Related: rhbz#1181568

* Tue Dec 09 2014 Peter Jones <pjones@redhat.com> - 0.6-3
- Add systemd scriptlets for the service.

* Thu Oct 09 2014 Peter Jones <pjones@redhat.com> - 0.6-2
- Require efivar >= 0.14-1 specifically.

* Wed Oct 08 2014 Peter Jones <pjones@redhat.com> - 0.6-1
- Update to 0.6
- make "dbxtool -l" correctly show not-well-known guids.

* Tue Oct 07 2014 Peter Jones <pjones@redhat.com> - 0.5-1
- Update to 0.5:
- make applying to dbx when it doesn't exist work (lersek)
- make displaying KEK work right

* Wed Aug 20 2014 Peter Jones <pjones@redhat.com> - 0.4-1
- First packaging attempt.

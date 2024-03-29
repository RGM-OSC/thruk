%global __os_install_post %{nil}
%global __perl_requires /bin/false 
%global __perl_provides /bin/false
%global __perllib_requires /bin/false
%global __perllib_provides /bin/false

Name: thruk
Version: 2.28.1
Release: 17.rgm
Summary: Thruk Monitoring Webinterface

Group: Applications/System
License: GPL
URL: http://www.thruk.org/
# download source from upstream: https://download.thruk.org/pkg/v2.28/src/thruk-2.28.tar.gz
Source0: thruk.tar.gz
Source1: %{name}-rgm.tar.gz
Source2: etc.tar.gz
Patch0:  %{name}-%{version}.patch
Patch1:  filter.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

Requires: httpd, mk-livestatus, mod_fcgid, perl, cairo >= 1.8.8, perl-Cpanel-JSON-XS
Requires: xorg-x11-server-Xvfb
Requires: systemd

# define path
%define datadir %{rgm_path}/%{name}-%{version}
%define linkdir %{rgm_path}/%{name}


%description
Thruk is an independent multibackend monitoring webinterface which currently supports Nagios, Icinga and Shinken as backend using the MKLivestatus addon.
It is designed to be a "dropin" replacement. The target is to cover 100% of the original features plus additional enhancements for large installations.

%prep
%setup -T -b 0 -n thruk
%patch0 -p1
%patch1 -p0
%setup -T -b 1 -n %{name}-rgm
%setup -T -b 2 -n etc

%install
cd %{_builddir}
rm -rf %{buildroot}
install -d -m0755 %{buildroot}%{datadir}
install -d -m0775 %{buildroot}%{datadir}/bp
install -d -m0755 %{buildroot}%{datadir}/logs
install -d -m0775 %{buildroot}%{datadir}/panorama
install -d -m0775 %{buildroot}%{datadir}/tmp
install -d -m0775 %{buildroot}%{datadir}/var
install -d -m0755 %{buildroot}%{_sysconfdir}/httpd/conf.d
install -d -m0755 %{buildroot}%{_sysconfdir}/cron.d
install -d -m0755 %{buildroot}%{_sysconfdir}/cron.daily
cp -afpvr %{_builddir}/%{name}/* %{buildroot}%{datadir}

# rgm specifics
install -d -m0755 %{buildroot}%{rgm_docdir}/%{name}
cp -afpvr %{_builddir}/%{name}-rgm/* %{buildroot}%{rgm_docdir}/%{name}
rm -rf %{buildroot}%{rgm_docdir}/%{name}/local-lib
rm -rf  %{buildroot}%{datadir}/plugins/plugins-enabled/conf
rm -rf  %{buildroot}%{datadir}/plugins/plugins-enabled/shinken_features
install -m 0644 %{_builddir}/%{name}-rgm/%{name}_local.conf %{buildroot}%{datadir}/%{name}_local.conf
install -m 0644 %{_builddir}/%{name}-rgm/cgi.cfg %{buildroot}%{datadir}/cgi.cfg
install -m 0644 -t %{buildroot}%{rgm_docdir}/%{name}/ %{name}-rgm/httpd-thruk.example.conf
install -m 0755 %{_builddir}/%{name}-rgm/fcgid_env.sh %{buildroot}%{datadir}/support/
install -m 0755 %{_builddir}/%{name}-rgm/phantomjs %{buildroot}%{datadir}/script/
install -m 0755 %{_builddir}/%{name}-rgm/pnp_export.sh %{buildroot}%{datadir}/script/
cp -afpvr %{_builddir}/%{name}-rgm/local-lib %{buildroot}%{datadir}/
cp -afpvr %{_builddir}/%{name}-rgm/RGM %{buildroot}%{datadir}/themes/themes-available/
cd %{buildroot}%{datadir}/root/thruk
ln -sf ../../themes/themes-enabled themes
cd %{buildroot}%{datadir}/themes/themes-enabled
ln -sf ../themes-available/RGM
#ln -sf ../themes-available/RGM %{buildroot}%{datadir}/root/thruk/themes/RGM
install -m 0644 %{_builddir}/etc/cron.d/thruk_logcache %{buildroot}%{_sysconfdir}/cron.d/thruk_logcache
install -m 0754 %{_builddir}/etc/cron.d/thruk_daily %{buildroot}%{_sysconfdir}/cron.daily/thruk_sanitization

%clean
rm -rf %{buildroot}

%post
sed -i '/use lib "\/srv\/rgm\/thruk\/lib";/d' %{datadir}/script/*.pl %{datadir}/script/thruk
sed -i '/use lib "\/srv\/rgm\/thruk\/local-lib\/lib\/perl5";/d' %{datadir}/script/*.pl %{datadir}/script/thruk
sed -i 's/use strict;/use lib "\/srv\/rgm\/thruk\/lib";\nuse lib "\/srv\/rgm\/thruk\/local-lib\/lib\/perl5";\n\nuse strict;/g' %{datadir}/script/*.pl %{datadir}/script/thruk
ln -nsf %{datadir} %{linkdir}
ln -s /srv/rgm/nagios/share/images/logos /srv/rgm/thruk/themes/themes-available/RGM/images/logos
if [ -e %{_sysconfdir}/httpd/conf.d/%{name}.conf ]; then
    rm -f %{_sysconfdir}/httpd/conf.d/%{name}.conf
fi
chown -h %{rgm_user_nagios}:%{rgm_group} %{linkdir}
chmod 775 %{datadir}/script 
chown apache:%{rgm_group} %{datadir}/bp 
chown apache:%{rgm_group} %{datadir}/panorama
chown apache:%{rgm_group} %{datadir}/tmp 
chown apache:%{rgm_group} %{datadir}/var 
touch /var/spool/cron/apache
chown apache:root /var/spool/cron/apache
chmod 600 /var/spool/cron/apache
systemctl restart httpd > /dev/null 2>&1

%postun
systemctl restart httpd > /dev/null 2>&1

%files
%doc %{rgm_docdir}/%{name}/httpd-thruk.example.conf
%defattr(-, root, root, 0755)
%{_sysconfdir}/cron.d/thruk_logcache
%{_sysconfdir}/cron.daily/thruk_sanitization
%config(noreplace) %{datadir}/thruk_local.conf
%config(noreplace) %{datadir}/cgi.cfg
%config(noreplace) %{datadir}/var/
%{rgm_docdir}/%{name}
%defattr(-, %{rgm_user_nagios}, %{rgm_group}, 0755)
%{datadir}


%changelog
* Thu Jul 07 2022 Christophe Cassan <ccassan@fr.scc.com> - 2.28-1-17.rgm
- Change css description width ellipsis 

* Sat Apr 23 2022 Eric Belhomme <ebelhomme@fr.scc.com> - 2.28-1-16.rgm
- introduce daily cronjob for SQL sanitization

* Thu Mar 11 2021 Eric Belhomme <ebelhomme@fr.scc.com> - 2.28-1-15.rgm
- move httpd config file as example file in /usr/share/doc/rgm/httpd/

* Thu Oct 29 2020 Michael Aubertin <maubertin@fr.scc.com> - 2.28-1-14.rgm
- Fix cron and logcache

* Thu Jun 04 2020 Michael Aubertin <maubertin@fr.scc.com> - 2.28-1-13.rgm
- Fix SSL version repport issues

* Fri May 29 2020 Michael Aubertin <maubertin@fr.scc.com> - 2.28-1-12.rgm
- Fix repport issues

* Thu Jan 16 2020 Michael Aubertin <maubertin@fr.scc.com> - 2.28-1-11.rgm
- Preparing RGM 1.2 to run side by side with RGMR :)

* Mon Apr 29 2019 Michael Aubertin <maubertin@fr.scc.com> - 2.28-1-10.rgm
- Fix the fix :) of ajax bug (add the fix also in cache for production environnement)

* Mon Apr 29 2019 Michael Aubertin <maubertin@fr.scc.com> - 2.28-1-9.rgm
- Fix ajax bug (service, hosts, and groups list)

* Mon Apr 29 2019 Michael Aubertin <maubertin@fr.scc.com> - 2.28-1-8.rgm
- Fix icon symlink

* Wed Apr 17 2019 Michael Aubertin <maubertin@fr.scc.com> - 2.28-1-7.rgm
- First RGM theme

* Sat Apr 13 2019 Michael Aubertin <maubertin@fr.scc.com> - 2.28-1-6.rgm
- Fix template issue and remove no longer used patch accordingly

* Fri Apr 12 2019 Michael Aubertin <maubertin@fr.scc.com> - 2.28-1-5.rgm
- Update initial config

* Fri Apr 12 2019 Michael Aubertin <maubertin@fr.scc.com> - 2.28-1-4.rgm
- Fix button look

* Fri Apr 12 2019 Michael Aubertin <maubertin@fr.scc.com> - 2.28-1-3.rgm
- Fix themes issues

* Wed Apr 10 2019 Michael Aubertin <maubertin@fr.scc.com> - 2.28-1-2.rgm
- Update themes

* Wed Apr 10 2019 Michael Aubertin <maubertin@fr.scc.com> - 2.28-1-1.rgm
- New release

* Tue Mar 19 2019 Eric Belhomme <ebelhomme@fr.scc.com> - 2.12-3-1.rgm
- use of rpm-macros-rgm
- fix config files
- fix ownerships

* Fri Mar 01 2019 Michael Aubertin <maubertin@fr.scc.com> - 2.12-3-0.rgm
- Initial fork 

* Thu Jan 19 2017 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 2.12-3-0.eon
- upgrade to version 2.12-3-0

* Mon Jun 27 2016 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 2.08-1.eon
- fix empty bp runtime

* Mon May 23 2016 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 2.08-0.eon
- upgrade to version 2.08-0

* Thu Jan 14 2016 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 2.04-1.eon
- upgrade to version 2.04-1

* Wed Nov 11 2015 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 2.04-0.eon
- upgrade to version 2.04-0

* Mon May 18 2015 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 1.88-4.eon
- upgrade to version 1.88-4

* Mon Mar 30 2015 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 1.86-4.eon
- upgrade to version 1.86-4

* Thu Feb 05 2015 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 1.86-3.eon
- upgrade to version 1.86-3

* Tue Oct 14 2014 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 1.84-6.eon
- upgrade to version 1.84-6

* Tue Jul 01 2014 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 1.84-4.eon
- upgrade to version 1.84-4

* Mon May 12 2014 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 1.84-0.eon
- upgrade to version 1.84-0

* Thu Mar 06 2014 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 1.82-0.eon
- upgrade to version 1.82-2

* Thu Sep 05 2013 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 1.76-0.eon
- upgrade to version 1.76-3

* Mon Jul 08 2013 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 1.74-0.eon
- upgrade to version 1.74
- eyesofnetwork path in pnp_export.sh script fix

* Sun Jun 23 2013 Michael Aubertin <michael.aubertin@gmail.com> - 1.72-3.eon
- Workaround (deal with tar) install rpm against new repport generator linked withtin static 64bits.

* Tue Jun 18 2013 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 1.72-2.eon
- upgrade to version 1.72-2

* Fri May 17 2013 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 1.70-3.eon
- upgrade to version 1.70-3

* Mon Apr 15 2013 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 1.68-0.eon
- upgrade to version 1.68

* Wed Jan 23 2013 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 1.62-1.eon
- pnp path for reports fix
- pnp time selector fix
- GD warnings fix

* Tue Jan 08 2013 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 1.62-0.eon
- upgrade to version 1.62

* Thu Nov 22 2012 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 1.58-0.eon
- upgrade to version 1.58

* Tue Oct 23 2012 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 1.54-0.eon
- upgrade to version 1.54

* Mon Oct 01 2012 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 1.50-0.eon
- upgrade to version 1.50

* Mon Sep 10 2012 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 1.46-0.eon
- upgrade to version 1.46

* Wed Aug 29 2012 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 1.44-0.eon
- upgrade to version 1.44

* Sun Jun 24 2012 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 1.34-0.eon
- upgrade to version 1.34

* Thu Jun 07 2012 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 1.32-0.eon
- upgrade to version 1.32

* Tue May 29 2012 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 1.30-0.eon
- upgrade to version 1.30

* Tue Apr 03 2012 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 1.26-0.eon
- upgrade to version 1.26

* Wed Mar 28 2012 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 1.24-0.eon
- upgrade to version 1.24

* Wed Mar 07 2012 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 1.22-0.eon
- upgrade to version 1.22

* Thu Feb 16 2012 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 1.18-0.eon
- upgrade to version 1.18

* Tue Jan 03 2012 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 1.1.7-0.eon
- upgrade to version 1.1.7

* Wed Sep 21 2011 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 1.1.1-0.eon
- upgrade to version 1.1.1

* Mon Aug 29 2011 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 1.1.0-0.eon
- upgrade to version 1.1.0

* Fri Jul 29 2011 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 1.0.7-0.eon
- upgrade to version 1.0.7

* Tue May 24 2011 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 1.0.4-0.eon
- upgrade to version 1.0.4

* Tue Mar 29 2011 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 0.90-0.eon
- upgrade to version 0.90

* Tue Mar 22 2011 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 0.86-0.eon
- upgrade to version 0.86

* Thu Mar 17 2011 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 0.84-0.eon
- upgrade to version 0.84

* Thu Feb 17 2011 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 0.82.1-0.eon
- xls export with special caracters fix
- french date fix
- livestatus over stunnel fix
- httpd logs path fix

* Tue Feb 08 2011 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 0.82-0.eon
- upgrade to version 0.82

* Mon Feb 07 2011 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 0.80-1.eon
- Eonweb statusmap link fix
- EyesOfNetwork theme fix

* Wed Feb 02 2011 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 0.80-0.eon
- packaged for EyesOfNetwork appliance

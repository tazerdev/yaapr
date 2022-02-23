# Get the semantic versioned tag of the git repository
%define version %(git describe --tags | awk -F\- {'print substr($1,2)'})

# Release is based on the number of commits since the cuurent tag was pushed.
# Since no commits returns blank and the rpm packaging guide says release should
# start at 1, we're going to do so using awk and increment the commit counts
# accordingly.
%define release %(git describe --tags | awk -F\- {'print ($2==""?"1":($2+1))'})

Summary:       Yet another ansible playbook runner.
Name:          yaapr
Version:       %{version}
Release:       %{release}%{?dist}
License:       GPLv3
Group:         Application/Automation
BuildArch:     noarch
Url:           https://github.com/tazerdev/yaapr.git
Requires:      python3 ansible git
BuildRequires: rpmdevtools rpm-build redhat-rpm-config python3-devel
Provides:      yaapr

%define topdir  %(echo $PWD)

%description
A utility for automating playbook runs in a decentralized fashion.

%prep
rm -rf %{buildroot}
rpmdev-setuptree

%install
install -m 0755 --directory %{buildroot}/etc/yaapr
install -m 0755 --directory %{buildroot}/etc/logrotate.d
install -m 0755 --directory %{buildroot}/etc/cron.daily
install -m 0755 --directory %{buildroot}/usr/bin
install -m 0755 --directory %{buildroot}/var/log/yaapr
install -m 0755 --directory %{buildroot}/var/lib/yaapr
install -m 0755 --directory %{buildroot}/var/lib/yaapr/cache

install -m 644 %{topdir}/etc/yaapr/yaapr.ini %{buildroot}/etc/yaapr
install -m 644 %{topdir}/etc/logrotate.d/yaapr %{buildroot}/etc/logrotate.d
install -m 755 %{topdir}/usr/bin/yaapr %{buildroot}/usr/bin
install -m 755 %{topdir}/etc/cron.daily/yaapr %{buildroot}/etc/cron.daily

# needed to prevent compiled python files from being included
exit 0

%files
%dir %attr(755, root, root) /etc/yaapr
%dir %attr(755, root, root) /var/log/yaapr
%dir %attr(755, root, root) /var/lib/yaapr
%dir %attr(755, root, root) /var/lib/yaapr/cache
%config %attr(644, root, root) /etc/yaapr/yaapr.ini
%attr(755, root, root) /usr/bin/yaapr
%attr(755, root, root) /etc/cron.daily/yaapr
%attr(644, root, root) /etc/logrotate.d/yaapr

%pre
if [ $1 == 1 ]
then
   # echo  "pre: Before RPM is installed"
   :
elif [ $1 == 2 ]
then
   # echo  "pre: Before RPM is upgraded"
   :
fi

%post
if [ $1 == 1 ]
then
   # echo "post: After RPM is installed"
   :
elif [ $1 == 2 ]
then
   # echo "post: After RPM is upgraded"
   :
fi

%preun
if [ $1 == 0 ]
then
   # echo "preun: Before RPM is removed/uninstalled"
   :
elif [ $1 == 1 ]
then
   # echo "preun: After RPM is upgraded but before cleanup"
   :
fi

%postun
if [ $1 == 0 ]
then
   # echo "postun: After RPM is removed/uninstalled"
   :
elif [ $1 == 1 ]
then
   # echo  "postun: After RPM is upgraded but after cleanup"
   :
fi

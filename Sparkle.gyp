# Copyright (c) 2015 ThinkChaos
# Released under the MIT license (see LICENSE)
# Inspired by: https://github.com/leiferikb/bitpop/blob/master/src/third_party/Sparkle/Sparkle_custom.gyp

{
  'variables': {
    'SUPPORTED_LOCALES': [
      'ar',
      'cs',
      'da',
      'de',
      'el',
      'en',
      'es',
      'fr',
      'is',
      'it',
      'ja',
      'ko',
      'nb',
      'nl',
      'pl',
      'pt_BR',
      'pt_PT',
      'ro',
      'ru',
      'sk',
      'sl',
      'sv',
      'th',
      'tr',
      'uk',
      'zh_CN',
      'zh_TW',
    ],
    'LOCALIZABLE_STRINGS': [
      '<!@(for l in <(SUPPORTED_LOCALES); do '
        'echo Sparkle/"$l".lproj/Sparkle.strings;'
      'done)',
    ],
    'LOCALIZABLE_XIBS': [
      '<!@(for l in <(SUPPORTED_LOCALES); do '
        'echo Sparkle/"$l".lproj/*.xib;'
      'done)',
    ],
  },
  'conditions': [
    ['OS=="mac"', {
      'targets': [
        {
          'target_name': 'Sparkle',
          'type': 'shared_library',
          'product_name': 'Sparkle',
          'mac_bundle': 1,
          'dependencies': [
            'Autoupdate',
          ],
          'configurations': {
            'Debug': {
              'xcode_config_file': 'Configurations/ConfigCommonDebug.xcconfig',
            },
            'Release': {
              'xcode_config_file': 'Configurations/ConfigCommonRelease.xcconfig',
            },
          },
          'xcode_settings': {
            # Configurations/ConfigFramework.xcconfig
            'DYLIB_INSTALL_NAME_BASE': '@rpath',
            'DYLIB_COMPATIBILITY_VERSION': '1.6',
            'DYLIB_CURRENT_VERSION': '$(SPARKLE_VERSION_MAJOR).$(SPARKLE_VERSION_MINOR).$(SPARKLE_VERSION_PATCH)',
            'PRODUCT_NAME': 'Sparkle',
            'WRAPPER_EXTENSION': 'framework',
            'FRAMEWORK_VERSION': 'A',
            'INFOPLIST_FILE': 'Sparkle/Sparkle-Info.plist',
            'GCC_PREPROCESSOR_DEFINITIONS': '$(inherited) BUILDING_SPARKLE=1',
            'OTHER_LDFLAGS': '-Wl,-U,_NSURLQuarantinePropertiesKey',
            'SKIP_INSTALL': 'YES',
          },
          'variables': {
            'public_headers': [
              'Sparkle/Sparkle.h',
              'Sparkle/SUAppcast.h',
              'Sparkle/SUAppcastItem.h',
              'Sparkle/SUErrors.h',
              'Sparkle/SUExport.h',
              'Sparkle/SUStandardVersionComparator.h',
              'Sparkle/SUUpdater.h',
              'Sparkle/SUVersionComparisonProtocol.h',
              'Sparkle/SUVersionDisplayProtocol.h',
            ],
            'private_headers': [
              '<!@(echo Vendor/**/*.h)',
              '<!@(echo Sparkle/*.h)',
            ],
          },
          'sources': [
            '<@(public_headers)',
            '<@(private_headers)',
            '<!@(echo Vendor/**/*.{c,m})',
            '<!@(echo Sparkle/*.h)',
          ],
          'mac_framework_headers': [
            '<@(public_headers)',
          ],
          'mac_bundle_resources': [
            '<@(LOCALIZABLE_STRINGS)',
            '<@(LOCALIZABLE_XIBS)',
            '<(PRODUCT_DIR)/Autoupdate.app',
            'Resources/SUModelTranslation.plist',
            'Sparkle/SUStatus.xib',
          ],
          'link_settings': {
            'libraries': [
              '$(SDKROOT)/System/Library/Frameworks/AppKit.framework',
              '$(SDKROOT)/System/Library/Frameworks/Foundation.framework',
              '$(SDKROOT)/System/Library/Frameworks/IOKit.framework',
              '$(SDKROOT)/usr/lib/libbz2.dylib',
              '$(SDKROOT)/usr/lib/libxar.1.dylib',
              '$(SDKROOT)/usr/lib/libz.dylib',
              '$(SDKROOT)/System/Library/Frameworks/Security.framework',
              '$(SDKROOT)/System/Library/Frameworks/SystemConfiguration.framework',
              '$(SDKROOT)/System/Library/Frameworks/WebKit.framework',
            ],
          },
          'postbuilds': [
            {
              'postbuild_name': 'Link fr_CA to fr',
              'action': [
                '/usr/bin/env', 'bash', '-c',
                'ln -fhs fr.lproj "$BUILT_PRODUCTS_DIR/$UNLOCALIZED_RESOURCES_FOLDER_PATH"/fr_CA.lproj',
              ],
            },
            {
              'postbuild_name': 'Link pt to pt_BR',
              'action': [
                '/usr/bin/env', 'bash', '-c',
                'ln -fhs pt_BR.lproj "$BUILT_PRODUCTS_DIR/$UNLOCALIZED_RESOURCES_FOLDER_PATH"/pt.lproj',
              ],
            },
          ],
        },
        {
          'target_name': 'Autoupdate',
          'type': 'executable',
          'product_name': 'Autoupdate',
          'mac_bundle': 1,
          'configurations': {
            'Debug': {
              'xcode_config_file': 'Configurations/ConfigCommonDebug.xcconfig',
            },
            'Release': {
              'xcode_config_file': 'Configurations/ConfigCommonRelease.xcconfig',
            },
          },
          'xcode_settings': {
            # Configurations/ConfigRelaunch.xcconfig
            'INFOPLIST_FILE': 'Sparkle/Autoupdate/Autoupdate-Info.plist',
            'PRODUCT_NAME': '$(SPARKLE_RELAUNCH_TOOL_NAME)',
            'SKIP_INSTALL': 'YES',
            'ASSETCATALOG_COMPILER_APPICON_NAME': 'AppIcon',
            'OTHER_LDFLAGS': '-Wl,-U,_NSURLQuarantinePropertiesKey',
          },
          'variables': {
            'headers': [
              'SUErrors.h',
              'SUHost.h',
              'SUInstaller.h',
              'SULog.h',
              'SUGuidedPackageInstaller.h',
              'SUPackageInstaller.h',
              'SUPlainInstaller.h',
              'SUPlainInstallerInternals.h',
              'SUStandardVersionComparator.h',
              'SUStatusController.h',
              'SUSystemProfiler.h',
              'SUWindowController.h',
            ],
          },
          'include_dirs': [
            'Sparkle',
          ],
          'sources': [
            '<@(headers)',
            'Sparkle/Autoupdate/Autoupdate.m',
            'Sparkle/SUConstants.m',
            'Sparkle/SUHost.m',
            'Sparkle/SUInstaller.m',
            'Sparkle/SULog.m',
            'Sparkle/SUGuidedPackageInstaller.m',
            'Sparkle/SUPackageInstaller.m',
            'Sparkle/SUPlainInstaller.m',
            'Sparkle/SUPlainInstallerInternals.m',
            'Sparkle/SUStandardVersionComparator.m',
            'Sparkle/SUStatusController.m',
            'Sparkle/SUSystemProfiler.m',
            'Sparkle/SUWindowController.m',
          ],
          'mac_bundle_resources': [
            '<@(LOCALIZABLE_STRINGS)',
            'Sparkle/SUStatus.xib',
            'Resources/Images.xcassets',
          ],
          'link_settings': {
            'libraries': [
              '$(SDKROOT)/System/Library/Frameworks/AppKit.framework',
              '$(SDKROOT)/System/Library/Frameworks/Foundation.framework',
              '$(SDKROOT)/System/Library/Frameworks/Security.framework',
            ],
          },
        },
      ],
    },],
  ],
}

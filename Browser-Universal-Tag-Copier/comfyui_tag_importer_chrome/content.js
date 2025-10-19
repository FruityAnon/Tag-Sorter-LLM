console.log('🎯 Universal Tag Copier loaded');

const siteConfigs = {
    'e621.net': {
        tagSelector: '.tag-list-item .tag-list-name',
        buttonPlacementSelector: '#tag-list',
        tagsToIgnore: ['artists', 'artist', 'species', 'general', 'copyright', 'character', 'meta', 'invalid', 'lore'],
        tagCleanup: (tagText) => tagText.trim()
    },
    'rule34.xxx': {
        tagSelector: '#tag-sidebar li.tag a:nth-of-type(2)',
        buttonPlacementSelector: '#tag-sidebar',
        tagsToIgnore: ['artist_name', 'twitter_username'],
        tagCleanup: (tagText) => tagText.trim()
    },
    'e6ai.net': {
        tagSelector: '#tag-list .tag-list-item .tag-list-name',
        buttonPlacementSelector: '#tag-list',
        tagsToIgnore: [],
        tagCleanup: (tagText) => tagText.trim()
    }
};

function getCurrentSiteConfig() {
    const hostname = window.location.hostname;
    for (const siteDomain in siteConfigs) {
        if (hostname.includes(siteDomain)) {
            return siteConfigs[siteDomain];
        }
    }
    return null;
}

function extractTags(config) {
    let tags = [];
    try {
        document.querySelectorAll(config.tagSelector).forEach(item => {
            const tagText = item.textContent;
            if (tagText) {
                const cleanedTag = config.tagCleanup(tagText);
                if (cleanedTag && !/^\d+[km]?$|^\d+\.\d+[km]?$/i.test(cleanedTag) && !config.tagsToIgnore.includes(cleanedTag.toLowerCase())) {
                    tags.push(cleanedTag);
                }
            }
        });
    } catch (error) {
        console.error('❌ Error extracting tags:', error);
    }
    return [...new Set(tags)].join(', ');
}

function addButton(config) {
    if (document.getElementById('universal-copy-btn')) return;
    const targetElement = document.querySelector(config.buttonPlacementSelector);
    if (!targetElement) {
        setTimeout(() => addButton(config), 1000);
        return;
    }
    const button = document.createElement('button');
    button.id = 'universal-copy-btn';
    button.textContent = '📋 Copy Clean Tags';
    button.style.cssText = `
        display: block; width: fit-content; margin: 10px 0; padding: 10px 14px; background: #2196F3; color: white;
        border: none; border-radius: 4px; cursor: pointer; font-size: 13px;
        font-family: Arial, sans-serif; font-weight: bold;
    `;
    button.addEventListener('click', function() {
        const tags = extractTags(config);
        if (!tags) {
            button.textContent = '❌ No Tags Found';
            setTimeout(() => button.textContent = '📋 Copy Clean Tags', 2000);
            return;
        }
        navigator.clipboard.writeText(tags).then(() => {
            button.textContent = '✅ Copied!';
            console.log(`✅ ${tags.split(',').length} tags copied to clipboard`);
            setTimeout(() => button.textContent = '📋 Copy Clean Tags', 2000);
        }).catch(err => {
            button.textContent = '❌ Copy Failed';
            console.error('Failed to copy: ', err);
            setTimeout(() => button.textContent = '📋 Copy Clean Tags', 2000);
        });
    });
    targetElement.parentNode.insertBefore(button, targetElement.nextSibling);
}

const config = getCurrentSiteConfig();
if (config) {
    addButton(config);
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
        if (request.action === "getTags") {
            const tags = extractTags(config);
            sendResponse({ tags: tags });
        }
    });
} else {
    console.log('⚠️ No configuration found for this site.');
}
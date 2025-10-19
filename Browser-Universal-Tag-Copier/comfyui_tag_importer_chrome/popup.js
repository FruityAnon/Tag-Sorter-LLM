document.addEventListener('DOMContentLoaded', function() {
  const copyBtn = document.getElementById('copyTags');
  const importBtn = document.getElementById('importTags');
  const statusDiv = document.getElementById('status');

  const supportedHosts = ['e621.net', 'rule34.xxx', 'e6ai.net'];

  function isOnSupportedPage(url) {
    try {
      const currentHost = new URL(url).hostname;
      const isSupportedHost = supportedHosts.some(host => currentHost.includes(host));
      const isPostPage = url.includes('/posts/') || url.includes('s=view');
      return isSupportedHost && isPostPage;
    } catch (e) {
      return false;
    }
  }

  function showStatus(message, type = 'info') {
    statusDiv.textContent = message;
    statusDiv.className = type;
  }

  function resetStatus() {
    statusDiv.textContent = 'Ready to import tags...';
    statusDiv.className = 'info';
  }

  copyBtn.addEventListener('click', () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const tab = tabs[0];

      if (!isOnSupportedPage(tab.url)) {
        showStatus('Please open a supported post page', 'error');
        setTimeout(resetStatus, 3000);
        return;
      }

      chrome.tabs.sendMessage(tab.id, { action: "getTags" }, (response) => {
        if (chrome.runtime.lastError) {
          console.error(chrome.runtime.lastError.message);
          showStatus('Error: Cannot access page content', 'error');
          setTimeout(resetStatus, 3000);
          return;
        }

        if (response && response.tags) {
          navigator.clipboard.writeText(response.tags).then(() => {
            const tagCount = response.tags.split(',').length;
            showStatus(`✅ Copied ${tagCount} tags!`, 'success');
          }).catch(err => {
            showStatus('❌ Failed to copy tags', 'error');
          }).finally(() => {
            setTimeout(resetStatus, 3000);
          });
        } else {
          showStatus('❌ No tags found on this page', 'error');
          setTimeout(resetStatus, 3000);
        }
      });
    });
  });

  importBtn.addEventListener('click', () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const tab = tabs[0];

      if (!isOnSupportedPage(tab.url)) {
        showStatus('Please open a supported post page', 'error');
        setTimeout(resetStatus, 3000);
        return;
      }

      showStatus('🔍 Checking ComfyUI...', 'info');

      chrome.runtime.sendMessage({ action: "checkComfyUI" }, (comfyCheck) => {
        if (chrome.runtime.lastError || !comfyCheck || !comfyCheck.success) {
          showStatus('❌ ComfyUI not available', 'error');
          setTimeout(resetStatus, 3000);
          return;
        }
        
        showStatus('📨 Getting tags from page...', 'info');
        chrome.tabs.sendMessage(tab.id, { action: "getTags" }, (tagResponse) => {
          if (chrome.runtime.lastError) {
            showStatus('❌ Error: Cannot access page content', 'error');
            setTimeout(resetStatus, 3000);
            return;
          }

          if (tagResponse && tagResponse.tags) {
            showStatus('📡 Sending tags to ComfyUI...', 'info');
            chrome.runtime.sendMessage({
              action: "saveTagsToFile",
              tags: tagResponse.tags,
              source: tab.url
            }, (result) => {
              if (chrome.runtime.lastError || !result || !result.success) {
                showStatus(`❌ Failed: ${result ? result.error : 'Unknown error'}`, 'error');
              } else {
                showStatus(`✅ ${result.data.tags_count} tags sent!`, 'success');
              }
              setTimeout(resetStatus, 3000);
            });
          } else {
            showStatus('❌ No tags found on page', 'error');
            setTimeout(resetStatus, 3000);
          }
        });
      });
    });
  });

  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const tab = tabs[0];
    if (tab && isOnSupportedPage(tab.url)) {
      showStatus('✅ Supported page detected', 'success');
    } else {
      showStatus('⚠️ Open a supported post page', 'warning');
      copyBtn.disabled = true;
      importBtn.disabled = true;
    }
  });
});